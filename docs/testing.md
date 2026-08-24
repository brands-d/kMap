# Testing

Plain `unittest`, discovered from the repo root. No pytest, no coverage tool,
no CI.

```bash
python -m unittest discover              # all of it, ~6 s
python -m unittest kmap.tests.test_orbital
python -m unittest kmap.tests.test_orbital.TestOrbital.test_get_kmap_basic
```

`make test-all` is the first of those. Run from the repo root — several tests
resolve fixtures relative to the test file, but discovery needs the root.

## What is there

| File | Tests | Covers |
|---|---|---|
| `test_orbital.py` | 9 | k-axes, the 3D-FT, and `get_kmap` under orientation, polarisation and symmetrization |
| `test_plotdata.py` | 15 | `PlotData` arithmetic, interpolation, smoothing, symmetrisation |
| `test_crosshair.py` | 11 | The crosshair models and their region cuts |
| `test_lmfit.py` | 9 | `LMFitModel`, ending in a full PTCDA fit |
| `test_misc.py` | 9 | Free functions in `library/misc.py` |
| `test_orbitaldata.py` | 4 | Loading from file and from hdf5, URL recognition, and **from the online database** |
| `test_sliceddata.py` | 1 | `SlicedData` from `.hdf5` |
| `test_application.py` | 1 | Constructs the `QApplication` — its body calls `kMap.test()`, which is `pass` |

59 tests total. The weight is where it should be: the numbers are pinned hard,
the GUI is not tested at all.

## The regression net for the physics

These are the assertions that make it safe to refactor `orbital.py`:

| Assertion | Where |
|---|---|
| 3D-FT shape, total sum and one element, to 13 decimals | `test_orbital.test_init_3DFT` |
| k-map shape, axis endpoints and `nansum`, to 13 decimals | `test_orbital.test_get_kmap_*` |
| PTCDA fit weights against `tests/output/weights_PTCDA`, to 5 decimals | `test_lmfit.test_PTCDA` |
| Background equation evaluation against `tests/output/background_expected` | `test_lmfit.test_background` |

Thirteen decimals means these fail on any real change to the calculation and
tolerate nothing. That is deliberate — see [physics.md](physics.md). If one of
them moves, **the change is wrong until proven otherwise**, whatever it looked
like in the diff.

Fixtures: `kmap/tests/input/pentacene_HOMO.cube` is the input for most of the
above; `kmap/tests/output/` holds the stored expectations.

## What is not tested

- **Every controller and every `.ui` file.** No window is ever opened by a
  test. A GUI change is proven only by running the app — use the `verify-app`
  skill.
- Project save/load (`.kmap` round-trip).
- The POV-Ray export.
- Anything about the database browser except the one download below.

## The one test that needs the network

`test_orbitaldata.test_online_initialization` fetches an orbital's
coefficients from the database and evaluates it. It **skips** when the request
fails, so an offline machine still gets a green suite. Everything else runs
offline.

Keep it that way: a test that needs the network skips, never fails.

## Adding a test

Put it in the file for the class under test. Name it so the name is the
documentation. If the test pins a number, say in a comment where the number
came from — a stored expectation with no provenance cannot be re-derived when
it eventually needs to change.
