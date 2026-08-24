# Architecture

## What it is

A PySide6 desktop application for photoemission orbital tomography. It
simulates momentum maps from molecular orbitals, displays measured ARPES data
sets, and fits one against the other. Published as
[Comput. Phys. Commun. 263, 107905 (2021)](https://doi.org/10.1016/j.cpc.2021.107905).

Everything runs in one process on the user's machine. There is no server, no
database and no background worker; the only network access is downloading
orbital data (see *Getting data in*).

## Stack

| | |
|---|---|
| GUI | PySide6 (Qt 6), layouts authored in QtCreator as `.ui` files |
| Plotting | pyqtgraph in the app, matplotlib for export windows, pyopengl for 3D |
| Numerics | numpy, scipy (`scipy.interpolate`, `scipy.ndimage`), scikit-image |
| Fitting | lmfit |
| Files | h5py for `.hdf5`, hand-rolled parser for `.cube`, `bz2` + `pickle` for `.kmap` projects |

Python ≥ 3.8. Installed with `setup.py`; there is no `pyproject.toml`, no
lockfile and no lint or format configuration in the repo (the source is
black-formatted, but black is not a declared dependency).

## Repository layout

```
kmap/
  __init__.py      __version__, __date__, __directory__ — imported everywhere
  kMap.py          the QApplication subclass; applies settings, opens MainWindow
  __main__.py      `python -m kmap`
  config/          the settings/logging/shortcut .ini files and the Config class
  library/         the domain layer: data classes and the physics
  model/           model classes (MVC) for the more complex controllers
  controller/      one class per feature/window; the bulk of the program
  ui/              .ui files and the pyside6-uic output generated from them
  resources/       icon, colormaps, and the README/about/welcome HTML
  tests/           unittest suites plus their input and expected-output fixtures
docs/              this directory
example/           example data and demo/tutorial scripts
dist/              built wheels and sdists of past releases (tracked)
```

`cli.py` and `kMap.spec` exist only for the PyInstaller build (`make package`).

The MVC split is real but not strict — plenty of controllers hold logic that
should be in a model, and `library/` holds a few things that are really
models. `docs/development-guide.txt` describes the intended pattern.

## The layers

### `library/` — the domain layer

This is the part worth understanding. It has no Qt imports of consequence and
is usable from a plain script; `example/scripts/` does exactly that.

| File | What it is |
|---|---|
| `orbital.py` | **The physics.** Reads a `.cube` (or hdf5) into ψ(r), 3D-FTs it, cuts hemispheres out of the result, applies the \|A·k\|² factor and symmetrization. See [physics.md](physics.md). |
| `plotdata.py` | A 2D image plus its axis ranges. Interpolation, smoothing, symmetrisation, arithmetic. Everything image-like in the app is one of these. |
| `sliceddata.py` | A 3D data set (two k-axes plus one of binding energy, photon energy or a spatial axis) with axis metadata. Built from experimental `.hdf5`, or generated from orbitals. |
| `axis.py` | One axis: label, units, range. |
| `abstractdata.py` | The `ID` / `name` / `meta_data` base shared by the data classes. |
| `orbitaldata.py` | `OrbitalData` = `Orbital` + `AbstractData`. Owns the loading paths: from file, and from the online database. |
| `database.py` | The online database at physikmdb.uni-graz.at: the listing the browser windows show, and the local evaluation of one orbital's ψ(r). |
| `misc.py` | Free functions: Euler matrices, `energy_to_k`, image arithmetic, cube writing, and the (legacy) remote-hdf5 client. |
| `colormap.py`, `id.py`, `qwidgetsub.py` | Colormap handling, ID generation, small QWidget subclasses. |
| `orbital2povray.py` | Standalone POV-Ray export. Large, self-contained, and unrelated to the rest. |

### `model/` — per-feature models

`lmfit_model.py` is the important one: a wrapper around lmfit that is also
usable as a module from a script (see `example/scripts/example5.py`). It holds
a `SlicedData`, a list of `OrbitalData`, the parameter set, the region
restriction and the background equation, and produces fitted weights.

The rest (`crosshair_model`, `colormap_model`, `pyqtgraphplot_model`, …) are
smaller and exist to keep data handling out of their controllers.

### `controller/` — the features

One class per GUI feature, each pairing with a `.ui` file of the same name and
following the `__init__` → `setupUi` → `_setup()` → `_connect()` pattern.

The ones to know:

| Class | Role |
|---|---|
| `mainwindow.py` | Menu bar, shortcuts, project save/load, all the file- and database-opening entry points. |
| `tabwidget.py` | Owns every tab and knows how to create, duplicate, save and restore each type. |
| `orbitaldatatab.py` | The simulation tab: a list of orbitals, orientation/polarisation controls, the resulting k-map. |
| `sliceddatatab.py` | The experiment tab: a 3D data set with a slider over its first axis. |
| `splitviewtab.py` | Two tabs side by side. |
| `lmfittab.py`, `lmfit*.py` | The fitting UI: parameter tree, options, results, result plots. |
| `databasewindows.py` | The online-database browser windows. |
| `profileplottab.py`, `miniplots.py`, `crosshair*.py` | Line/region profiles and the crosshair tools that drive them. |

### `ui/` — generated code

Each `foo.ui` (XML, authored in QtCreator) has a generated `foo.py` beside it.
**The `.py` files are generated and must not be hand-edited** — see the
`ui-change` skill.

### `config/`

`config.py` defines a module-level singleton `config`, imported as
`from kmap.config.config import config`. It reads each `*_default.ini` and
then the matching `*_user.ini` on top, so a user file only needs the keys it
overrides. `config.get_key(group, key)` always returns a **string**; callers
convert.

`*_user.ini` files are created empty on first run and are gitignored.

## How a momentum map reaches the screen

1. `OrbitalData.init_from_file` / `init_from_online` produces an `OrbitalData`.
2. Its `Orbital.__init__` parses the cube into `self.psi` (grid + ψ values) and
   `self.molecule` (atoms), then `compute_3DFT` pads and FFTs it into
   `self.psik` — done **once**, and it is the expensive step.
3. `OrbitalTable` in the simulation tab holds one row per orbital with its
   weight and Euler angles.
4. On any control change, `OrbitalDataTab` asks each orbital for
   `get_kmap(E_kin, dk, phi, theta, psi, Ak_type, …)`.
5. `get_kmap` interpolates a hemisphere of radius k(E_kin) out of `psik`,
   rotates it by the Euler angles, symmetrises, multiplies by \|A·k\|², and
   returns a `PlotData`. Each of those four stages is cached and recomputed
   only when its own `check_new_*` says a parameter changed.
6. The weighted sum of the orbitals' `PlotData` is interpolated onto the
   display grid and handed to `PyQtGraphPlot`.

## Getting data in

| Source | Path |
|---|---|
| Local `.cube` | `OrbitalData.init_from_file`, searching `paths.cube_start` and the comma-separated `paths.path` |
| Local `.hdf5` (experiment) | `SlicedData.init_from_hdf5` |
| Online database | The browser windows in `databasewindows.py` → `OrbitalData.init_from_online` / `SlicedData.load_orbital_online` |
| Project file | `.kmap`, a `bz2`-compressed pickle of each tab's `save_state()` |

The online path goes through the `physikmdb` package: the site serves GTO
coefficients rather than cube files, so ψ(r) is evaluated locally and reaches
`Orbital` as a `(psi, molecule)` pair (`file_format="psi"`). See
[conventions.md](conventions.md#the-online-database).

## Configuration and logging

Logging is configured from `logging_default.ini` through
`logging.config.fileConfig` at startup; everything logs to the `"kmap"`
logger, obtained ad hoc as `logging.getLogger("kmap")`. The default handler
writes `default.log` in the working directory, which is why `*.log` is
gitignored.
