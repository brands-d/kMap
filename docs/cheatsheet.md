# Cheatsheet

The virtual environment lives in the **main checkout** and is shared by every
worktree:

```bash
source /Users/dominik/lib/kMap/.venv/bin/activate
```

Everything below assumes it is active and the working directory is the repo
root.

## Run

```bash
python -m kmap
```

`make run` is the same thing.

## Test

```bash
python -m unittest discover                       # all, ~6 s
python -m unittest kmap.tests.test_orbital        # one file
python -m unittest kmap.tests.test_orbital.TestOrbital.test_get_kmap_basic
```

## Regenerate the UI

After editing a `.ui` file in QtCreator:

```bash
cd kmap/ui && ./compile_interface.sh     # regenerates every .py from its .ui
pyside6-uic mainwindow.ui -o mainwindow.py   # or just the one you changed
```

Open a layout for editing:

```bash
pyside6-designer kmap/ui/mainwindow.ui
```

## Install and package

```bash
make setup       # fresh venv in ./venv (the repo's own convention)
make install     # pip install --upgrade pip; python setup.py install
make build       # sdist + wheel into dist/
make package     # PyInstaller one-folder build (Windows paths in the Makefile)
make clean       # remove build/, *.egg-info, *.log, report.tar.gz
```

## Diagnostics

```bash
make report      # runs the tests and tars the logs + user settings
make generate-uml # pyreverse class/package diagrams (needs pylint installed)
tail -f default.log
```

## The database API by hand

```bash
curl -s https://physikmdb.uni-graz.at/api/filters
curl -s https://physikmdb.uni-graz.at/api/systems
curl -s https://physikmdb.uni-graz.at/api/calculations
curl -s https://physikmdb.uni-graz.at/api/calculations/21   # + its orbitals
```

`/api/calculations` is the full listing (~1070 rows, ~540 kB); orbitals come
only from the per-calculation route.

```python
from kmap.library.database import connect, load_orbital

psi, molecule = load_orbital("physikmdb://18/72")   # what kMap actually calls
db = connect()                            # or connect("http://127.0.0.1:5001")
calc = db.calculation(21)
calc.orbitals
psi = calc.wavefunction("HOMO", extent=8.0, points=64)   # [iz, iy, ix]
```

## Settings

```
kmap/config/settings_default.ini    # read this, never edit
kmap/config/settings_user.ini       # edit this, gitignored
```

Useful ones while working: `app.check_for_updates`, `paths.cache`,
`paths.path`, `orbital.dk3D`, `orbital.dk`, `orbital.grid_spacing`,
`orbital.grid_padding`, `database.url`.
