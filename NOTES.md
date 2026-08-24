# Notes

Facts a later session needs and cannot read off the code. Delete an entry once
the code says it.

- **The new database path is validated against the old one.** Calculation 18
  (5A, NWChem B3LYP/6-31G\*) is the calculation that produced
  `kmap/tests/input/pentacene_HOMO.cube`: the geometries agree to 3e-7 Å.
  Locally evaluated ψ(r) reproduces that cube to ~1e-3 of its peak, and the
  resulting k-maps agree to **0.2 % at the default `dk3D=0.12`**, falling to
  0.05 % at `dk3D=0.08` — i.e. the residual is kMap's own 3D-FT interpolation,
  not the data. Checked for `Ak_type` `no`/`NanoESCA`/`toroid`, tilted
  orientations, unpolarised light and 2-fold+mirror symmetrization.

- **The old site is gone.**
  `http://physikmdb.uni-graz.at/molecule_database_as_txt/MolecularOrbitals.txt`
  and the `cubefiles/…` URLs time out rather than returning an error.
  `https://physikmdb.uni-graz.at` serves the replacement application.

- **physikmdb's download cache is keyed by storage folder only, not by
  instance.** A `basis.bin` cached from a local dev server is served for the
  public site's calculation of the same number, silently and with completely
  different physics — this was observed on this machine (calculation 1 came
  back as naphthalene rather than benzene). `database.connect()` works around
  it with a per-URL cache directory. Reported upstream; drop the workaround
  once the package keys its own cache properly.

- **physikmdb only evaluates cubic boxes.** `kernels.scalar_field` takes one
  `points` and one `spacing`, so the grid is a cube reaching past the furthest
  atom, where the old cube files were rectangular and fitted to the molecule.
  Rectangular support is requested upstream. It costs only the field
  evaluation: `compute_3DFT` pads to a size fixed by `dk3D` and `dx`, so the
  FFT is the same size either way.
