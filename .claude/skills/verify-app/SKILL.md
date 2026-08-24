---
name: verify-app
description: Run kMap.py and prove a GUI change actually works. Use after any change to kmap/controller/, kmap/ui/, kmap/model/ or a window's behaviour — the Qt layer has essentially no test coverage, so the running application is the check.
---

# Verify the app

58 tests, and not one of them opens a window. Every controller, every `.ui`
file and every signal connection is unverified until something runs it. "The
tests pass" says nothing about a GUI change.

## Setup

The venv lives in the main checkout and is shared by worktrees:

```bash
source /Users/dominik/lib/kMap/.venv/bin/activate
```

kMap is **not installed** into it — imports resolve because the repo root is
on `sys.path`. So run from the repo root, or set
`PYTHONPATH=<repo root>` for a script that lives elsewhere.

Turn off the two startup network calls while working. `settings_user.ini` is
gitignored and worktree-local:

```ini
[app]
check_for_updates=False
auto_update_database=False
```

Without this, startup blocks for **75 seconds** on the dead database URL
before the window appears (see `NOTES.md`).

## Headless: drive the real widgets

The fastest and most useful check. `QT_QPA_PLATFORM=offscreen` constructs the
actual `MainWindow`, tabs and controllers with no display, so you can call
slots and assert on state:

```python
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from kmap.controller.mainwindow import MainWindow

app = QApplication([])
win = MainWindow()
tabs = win.tab_widget.tab_widget          # the inner QTabWidget

win.open_orbital_data_tab()
tab = win.tab_widget.get_current_tab()
print(type(tab).__name__, tabs.count(), tabs.tabText(tabs.count() - 1))
```

`QOpenGLWidget is not supported on this platform` and
`This plugin does not support propagateSizeHints()` are expected on the
offscreen backend and are not your bug. Anything else in that output is.

This catches the failures that actually happen here: a signal wired to a slot
that no longer exists, a widget renamed in the `.ui` but not in the
controller, an exception swallowed by one of the bare `except:` blocks.

Put throwaway scripts in the scratchpad directory, not in the repo.

## On screen

For anything visual — layout, a new control, a plot — it has to be looked at:

```bash
python -m kmap
```

Then drive it by hand. Watch `default.log` in another shell; the controllers
log more than they show, and `TabWidget` catches load failures and only logs
them:

```bash
tail -f default.log
```

**Claude cannot see this window.** `screencapture` is refused without screen
recording permission for the terminal. So: do the headless check yourself,
then describe exactly what the user should click and what they should see —
do not claim a visual result you have not observed.

Leave no instance running when you hand work back:

```bash
pkill -f "python -m kmap"
```

## What to actually exercise

Whatever you touched, plus the paths that share code with it:

| Changed | Check |
|---|---|
| A controller or its `.ui` | Open that window; use every control you touched |
| `tabwidget.py` | Open the tab, duplicate it, rename it, close it, and save + reload a project |
| Anything reached from a menu | The menu entry *and* its keyboard shortcut (`shortcut_default.ini`) |
| The database browser | Open it, filter, select a molecule and an orbital, load, and cancel out of it |
| Loading code | A local `.cube`, a local `.hdf5`, and the online path |
| Anything that ends up in `save_state()` | Save a `.kmap`, restart, load it |

The last one matters more than it looks: `.kmap` files are pickles of live
objects, so a renamed attribute breaks every project a user already has.

## Reporting

Say which of the two paths you used. If you only ran headless, say so — it
proves the wiring, not the appearance.
