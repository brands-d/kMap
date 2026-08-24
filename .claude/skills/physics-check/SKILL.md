---
name: physics-check
description: Validate anything that touches the physics — kmap/library/orbital.py, the 3D-FT, the hemispherical cut, |A·k|², symmetrization, unit conversions, or a new source of ψ(r). Use before claiming a physics-affecting change is correct, and when writing numerical tests.
---

# Physics check

kMap.py's current output is the ground truth. It has been used and checked by
many people over years, and the parts that matter most were contributed by a
domain expert. A change that alters a momentum map has not improved the
program — it has broken it, in the one way nobody will report.

So the standard is not "the code looks right". It is **the numbers did not
move**, demonstrated.

## When this applies

- `kmap/library/orbital.py` — any of it.
- `energy_to_k`, `compute_Euler_matrix`, `write_cube` in `library/misc.py`.
- `PlotData.interpolate`, `.smooth`, `.symmetrise`.
- `model/lmfit_model.py` where it builds or weights k-maps.
- Any unit conversion, anywhere.
- Any **new source of ψ(r)** — a new file format, a new download path, a
  locally evaluated wavefunction. Getting a grid subtly wrong here is
  indistinguishable from getting the physics wrong.

## Before you change anything

Run the suite and record that it is green:

```bash
python -m unittest discover
```

If something is already failing, note which and why before starting. You
cannot tell what you broke otherwise.

## The check

The regression net is already sharp — use it rather than inventing one.

```bash
python -m unittest kmap.tests.test_orbital kmap.tests.test_lmfit
```

| Assertion | Tolerance |
|---|---|
| 3D-FT shape, total sum, one element (`test_init_3DFT`) | 13 decimals |
| k-map shape, axis endpoints, `nansum` (`test_get_kmap_*`) | 13 decimals |
| PTCDA fit weights vs `tests/output/weights_PTCDA` (`test_PTCDA`) | 5 decimals |

Thirteen decimals tolerates nothing. **If one of these moves, the change is
wrong until proven otherwise** — not "the test needs updating". Stop and say
so.

A stored expectation is only ever changed with the user's explicit agreement,
in its own commit, with the reason and the derivation of the new number
written into the commit message.

## When the tests do not reach it

They pin sums and single elements of one orbital. That is a strong net and not
a complete one. If your change is somewhere they do not reach, pin it yourself
before and after:

```python
from kmap.library.orbital import Orbital

with open("kmap/tests/input/pentacene_HOMO.cube") as f:
    orbital = Orbital(f.read())

kmap = orbital.get_kmap(E_kin=30, dk=0.03, phi=0, theta=0, psi=0,
                        Ak_type="NanoESCA", polarization="p",
                        angle=60, azimuth=90, gamma="auto")
print(kmap.data.shape, np.nansum(kmap.data))
```

Save the full array with `np.save` on the unmodified code, then compare
against it afterwards with `npt.assert_allclose(..., rtol=0, atol=0)`. An
exact comparison is the right one: a refactor that is genuinely
behaviour-preserving reproduces floats bit for bit.

Vary what your change touches — several `E_kin`, a rotated orientation, each
`Ak_type`, each symmetrization — not just the default path.

## A new source of ψ(r)

Everything downstream reads exactly two dicts, so validate those directly:

```python
orbital.psi       # name, nx/ny/nz, dx/dy/dz, x/y/z, data
orbital.molecule  # num_atom, chemical_numbers, atomic_coordinates
```

Check, in this order:

1. **Units.** `psi["x"]` and `atomic_coordinates` are Ångström. Cube files
   are Bohr and are converted on read; a factor of 0.529 here is a factor
   of 1.9 in every k-map.
2. **Index order.** `psi["data"]` is `[ix, iy, iz]`, x slowest. Any source
   that produces `[iz, iy, ix]` needs a transpose, and the result of getting
   it wrong is a plausible-looking transposed map.
3. **Centring.** The grid runs `-l/2 … +l/2` and the atoms are shifted to
   match. Compare `atomic_coordinates` against the molecule's known geometry.
4. **The array itself.** Against a reference cube for the same orbital,
   element by element:

   ```python
   npt.assert_allclose(new.psi["data"], reference.psi["data"], rtol=1e-5)
   ```

   Sign is allowed to differ globally — the overall phase of an MO is
   arbitrary and `abs2` discards it. A sign difference that varies across the
   grid is a bug.
5. **The k-map**, last: same orbital through both paths, compared as above.

`example/data/` and `kmap/tests/input/` hold cube files whose provenance is
known; they are the references.

## Reporting

Say what you ran and what it showed. "Tests pass" is not a physics check —
name the comparison and the tolerance. If you could not demonstrate a
physics-affecting change is right, say that plainly instead of shipping it.
