# The calculation

Everything here lives in `kmap/library/orbital.py`, with a few free functions
in `kmap/library/misc.py`. **This is the part of the program that must not
change its output.** Read [../CLAUDE.md](../CLAUDE.md) and use the
`physics-check` skill before editing any of it.

The method is the plane-wave final state approximation described in
[Comput. Phys. Commun. 263, 107905 (2021)](https://doi.org/10.1016/j.cpc.2021.107905).

## Units

| Quantity | Unit | Where it is set |
|---|---|---|
| Energies (`E_kin`, orbital energy, work function, `V0`) | eV | throughout |
| Real-space grid and atomic coordinates | Å | converted on read |
| Momenta (`k`, `dk`, `k_max`, `gamma`) | Å⁻¹ | throughout |
| Angles (`phi`, `theta`, `psi`, `angle`, `azimuth`) | degrees | converted to rad at use |

Cube files store Bohr. `Orbital._read_cube` multiplies by
`b2a = 0.529177105787531` on the way in and **nothing above it ever sees
Bohr**. That single conversion is the whole unit boundary — keep it that way.

`energy_to_k(E_kin)` in `misc.py` is the other conversion: √(2mE)/ℏ with the
CODATA constants written out inline, giving Å⁻¹ from eV.

## The pipeline

### 1. ψ(r) — `_read_cube` / `_read_local_hdf5`

Produces two dicts and nothing else:

```python
self.psi      # name, nx/ny/nz, dx/dy/dz, x/y/z (1D grids), data (nx, ny, nz)
self.molecule # num_atom, chemical_numbers, atomic_coordinates (num_atom, 3)
```

`data` is indexed `[ix, iy, iz]`, x slowest — the order a cube file is written
in. Anything supplying ψ from another source must match that.

**The box is re-centred on the origin** (since 2022-08-08): `x`, `y`, `z` run
from `-l/2` to `+l/2` regardless of the cube's stated origin, and the atomic
coordinates are shifted by the same amount so the molecule stays put relative
to the orbital. The cube's own origin is discarded.

### 2. ψ̃(k) — `compute_3DFT`

Called once from `__init__`, and the expensive step.

- Zero-pads each axis until the resulting k-resolution reaches `dk3D`
  (`orbital.dk3D`, default 0.12 Å⁻¹): `pad = 2π/(dk3D·dx) − nx`, rounded up to
  even. Padding is symmetric, then `ifftshift` puts the box centre at index 0.
- `np.fft.fftn`, then `fftshift`.
- Normalised so that `Σ|ψ̃|² · dkx·dky·dkz = 1`.
- Cropped to |k| ≤ k(`E_kin_max`) (`orbital.E_kin_max`, default 150 eV) to
  keep the array manageable.
- Reduced to a real array by `value`: `'real'`, `'imag'`, `'abs'`,
  `'complex'`, or the default `'abs2'` = |ψ̃|². `OrbitalData` always uses
  `'abs2'`; the other modes exist for the scripts and the POV-Ray export.
- Wrapped in a `scipy.interpolate.RegularGridInterpolator` with
  `fill_value=np.nan` — the NaNs outside the FT box are what you see when a
  hemisphere is asked for beyond `E_kin_max`.

Result in `self.psik`: `kx`, `ky`, `kz`, `data`, `data_interp`.

Note that `dk3D` changes the FFT grid and therefore the interpolation, so it
changes the numbers. It is a resolution knob, not a display setting.

### 3. The hemisphere — `set_kinetic_energy`

A photoelectron of kinetic energy `E_kin` leaves with |k| = k(E_kin), so the
measurable data is a spherical cap through ψ̃. On a (kx, ky) grid of spacing
`dk` out to ±k(E_kin):

```
KZ = sqrt(k_V² − (k_V²/kmax²)·(KX² + KY²))
```

with `kmax = energy_to_k(E_kin)` and `k_V = energy_to_k(E_kin + V0)`. `V0` is
the inner potential; at `V0 = 0` this is the plain hemisphere
`KZ = sqrt(kmax² − KX² − KY²)`.

`dk` may also be a `(kxi, kyi)` tuple of explicit grids, which is how the
fitting code cuts straight onto the experiment's own grid instead of
interpolating twice.

### 4. Orientation — `set_orientation`

Rotates the hemisphere (not the molecule) by Euler angles φ, θ, ψ, using
`compute_Euler_matrix` in `misc.py` — Eq. (M3.10.3) of Lang–Pucker.

### 5. Symmetrization — `set_symmetry`

`'no'`, `'2-fold'`, `'3-fold'`, `'4-fold'`, each optionally `'+mirror'`.
Delegates to `PlotData.symmetrise`.

**It mutates `self.kmap["data"]` in place.** It is only correct because
`get_kmap` always re-runs `set_orientation` (which regenerates the data)
before it. Do not call it twice on one cut.

### 6. |A·k|² — `set_polarization`

The light–matter matrix element, multiplied onto the cut.

- `Ak_type`: `'no'` (factor ≡ 1), `'toroid'`, `'NanoESCA'`, and the
  `'only-…'` variants that return the factor alone for inspection.
- `polarization`: `'p'`, `'s'`, `'unpolarized'`, `'C+'`, `'C-'`, `'CDAD'`.
- `angle` / `azimuth`: the plane of incidence, in degrees.
- `s_share`: the s-polarised fraction for `'unpolarized'`, 0–1.
- `gamma`: final-state damping in Å⁻¹. `gamma='auto'` uses the empirical
  "universal curve" λ = 10·(143·E⁻² + 0.054·√E) Å with E in eV, so γ = 1/λ.

The toroid geometry differs from NanoESCA in that the electron stays in the
plane of incidence and the sample rotates instead.

## Caching, and how to break it

`get_kmap` recomputes each stage only when its `check_new_*` method reports a
change:

| Stage | Guard | Cached in |
|---|---|---|
| hemispherical cut | `check_new_cut(E_kin, dk, V0)` | `self.kmap` |
| orientation | `check_new_orientation(phi, theta, psi)` | `self.kmap` |
| symmetrization | `check_new_symmetrization(symmetrization)` | `self.kmap` |
| \|A·k\|² | `check_new_Ak(Ak_type, polarization, angle, azimuth, gamma, s_share)` | `self.Ak` |

**Adding a parameter to a `set_*` method without adding it to the matching
`check_new_*` produces a display that silently keeps showing the previous
result.** This is the single easiest way to introduce a wrong number here, and
it will not fail a test.

## Where the numbers are pinned

- `kmap/tests/test_orbital.py` — `get_kmap` against stored expectations.
- `kmap/tests/output/weights_PTCDA` — a full fit result, in `test_lmfit.py`.
- `kmap/tests/input/pentacene_HOMO.cube` and `example/data/*.cube` — the
  reference inputs.

These are the contract. See [testing.md](testing.md).
