# Conventions and gotchas

Things that are true, matter, and are not obvious from reading one file.

## Generated files

`kmap/ui/*.py` are produced by `pyside6-uic` from the `.ui` file of the same
name. They are tracked (the package must install without QtCreator) and they
are **never hand-edited**. See the `ui-change` skill.

`docs/classes_kMap.png` and `docs/packages_kMap.png` come from
`make generate-uml` and are stale. Trust the code.

## Configuration

- `config` is a module-level singleton: `from kmap.config.config import config`.
- `config.get_key(group, key)` returns a **string**, always. Callers do
  `int(...)`, `float(...)`, or compare against `"True"` / `"None"` as strings.
  `config.set_key` exists and is a no-op.
- `*_default.ini` is the full set; `*_user.ini` overrides key by key and may
  contain only what the user changed. Renaming a default key silently discards
  that user's setting.
- `*_user.ini` files are created empty on first run and are gitignored
  (`*_user*`).
- Settings are re-read at runtime by *Preferences → Reload Settings*, which
  calls `kMap.load_settings()`. Not every setting is honoured on reload — the
  font and the pyqtgraph options are, most others are read once at
  construction.

## Paths

- `kmap/__init__.py` exports `__directory__`, the absolute path of the `kmap`
  package. Relative paths in the `.ini` files are resolved against it.
- `paths.path` is a comma-separated search list, used like `PATH`, for finding
  `.cube` files by name.
- `paths.cache` defaults to `None`, i.e. **caching is off**. Where the code
  writes a cache it first checks `os.path.isdir(cache_dir)`, so an unset or
  missing directory silently disables it rather than failing.

## Data classes

- `AbstractData` gives every data object an `ID`, a `name` and a `meta_data`
  dict. IDs come from `library/id.py` and are what tabs, tables and fit
  results refer to each other by.
- `meta_data` is a free-form dict that travels with the object into tooltips,
  exported `.hdf5` and saved projects. Keys added there are effectively public.
- `PlotData` carries `data` plus its `x_axis`/`y_axis` ranges. Its methods
  take `update=True` to mutate in place and return a new object otherwise —
  check which one a call site wants.

## Saved projects

`.kmap` files are `bz2` + `pickle` of whatever `save_state()` returned for
each tab. That means the pickled attribute names *are* the file format:
renaming or removing an attribute that ends up in a save makes existing
project files unloadable. `TabWidget.save_state`/`restore_state` and each
tab's own pair are the places to look before changing one.

Loading a `.kmap` unpickles arbitrary objects from the file. That is fine for
a user's own saves and would not be for a file from a stranger.

## Qt

- Controllers follow `__init__` → `super().__init__()` → `setupUi(self)` →
  `_setup()` → `_connect()`. `docs/development-guide.txt` explains why.
- The inheritance order `class Foo(QWidget, Foo_UI)` is not arbitrary.
- **Do not use lambdas in `connect()`.** The guide is explicit: it keeps the
  object alive and leaks. Add a signal of your own instead.
- Windows opened from `MainWindow` are kept alive in `self.sub_windows` keyed
  by `id()`; they set `Qt.WA_DeleteOnClose` and call `deleteLater()` in
  `closeEvent`. Forgetting the reference means the window vanishes
  immediately.
- `DatabaseWindowBase.closeEvent` emits `files_chosen` on *every* close,
  including a cancel — the receiving slots handle an empty list.

## Numerics

- `np.seterr(invalid="ignore")` is set at import of `orbital.py`. Invalid
  operations produce NaN silently, on purpose: the region outside the FT box
  is NaN and gets summed with `np.nansum`. Do not "fix" a NaN warning by
  changing this.
- Array index order in the plotting layer depends on pyqtgraph's
  `imageAxisOrder`, set from the config at startup.
- `library/misc.py` mixes genuinely general helpers with two or three that are
  only used once. Do not assume a function there is widely used before
  grepping.

## Logging

One logger, `"kmap"`, fetched ad hoc wherever it is needed:

```python
log = logging.getLogger("kmap")
log.info("...")
```

Configured from `logging_default.ini` at startup. Writes `default.log` in the
working directory; `*.log` is gitignored. `make report` bundles the log and
the user settings for a bug report.

## The online database

`kmap/library/database.py` talks to physikmdb.uni-graz.at through the
`physikmdb` package. The site serves the **coefficients** of an LCAO-GTO
expansion, not cube files, so ψ(r) is evaluated locally by that package and
handed to `Orbital` as `file_format="psi"` — a `(psi, molecule)` pair rather
than cube text.

Vocabulary, because it changed and the code straddles both:

- What the old bundled listing called a **molecule** — it carried a basis set
  and an XC-functional — is what the new database calls a **calculation**.
  Its **system** is the molecule. One system has many calculations.
- `library/database.Molecule` therefore wraps one *calculation*, and its `ID`
  is the calculation id — the number in an entry page's URL.

Things worth knowing:

- **Only ground-state calculations are listed.** The database also holds
  TD-DFT (casida) runs, which kMap has no use for.
- **Only the frontier orbitals are listed** — `orbital_window` above and below
  the HOMO. A calculation holds every orbital it computed, which runs to
  hundreds.
- **A molecule's orbitals are fetched when its tree row is expanded**, not
  when the window opens. Listing 1000 calculations eagerly would be 1000
  requests.
- **Three URL forms reach `load_orbital`:** `physikmdb://<calculation>/<index>`
  is what the browser hands out; an old `…/cubefiles/<legacy id>/<name>_MO_<n>`
  URL is translated via the calculation's `legacy_id`, so projects saved
  before the switch still find their orbitals; anything else is treated as a
  plain cube file to download, which is what the URL box in the browser is
  for.
- **The grid is a cube centred on the origin**, `orbital.grid_spacing` apart
  and reaching `orbital.grid_padding` beyond the furthest atom. It is cubic
  because `physikmdb` only evaluates cubic boxes; a rectangular box fitted to
  the molecule would be cheaper and is requested upstream. It costs the
  evaluation only — `compute_3DFT` pads to a size set by `dk3D` and `dx`, so
  the FFT is the same size either way.
- **`connect()` gives the client its own cache directory, per instance URL.**
  The `physikmdb` package keys its download cache by the calculation's storage
  folder alone, so a `basis.bin` cached from a local dev server will otherwise
  be served for the public site's calculation of the same number — silently,
  and with entirely different physics. Never construct `physikmdb.Database`
  directly.

`library/misc.get_remote_hdf5_orbital` and `Orbital.init_from_remote_hdf5`
talk to an h5serv instance at `143.50.187.12:80`. Database URLs no longer
reach it, but a plain cube URL still tries it first inside a bare `except:`,
so its failure is invisible. Left in place for now; see
[../ISSUES.md](../ISSUES.md).
