---
name: ui-change
description: Change a window's layout or widgets in kMap.py — the .ui / pyside6-uic loop. Use whenever a task needs a new control, a renamed widget, or any edit under kmap/ui/, so the generated .py files are never hand-edited.
---

# Changing a window

Every window is a pair: `kmap/ui/foo.ui` (XML, authored in QtCreator) and
`kmap/ui/foo.py` (generated from it by `pyside6-uic`), imported by
`kmap/controller/foo.py`.

**The `.py` is generated. Never edit it.** It is tracked so the package
installs without QtCreator, which makes it look editable. Any change you make
there is lost the next time anyone regenerates, and the `.ui` — the actual
source — silently disagrees with the shipped code in the meantime.

## The loop

1. Edit the `.ui`:

   ```bash
   pyside6-designer kmap/ui/foo.ui
   ```

   Or edit the XML directly for something small and mechanical — a renamed
   `objectName`, a changed range, a new label. It is readable XML, and for a
   one-attribute change that is less risky than a Designer round-trip, which
   reformats and reorders whole blocks and makes the diff unreadable.

2. Regenerate:

   ```bash
   pyside6-uic kmap/ui/foo.ui -o kmap/ui/foo.py
   ```

   `kmap/ui/compile_interface.sh` regenerates all of them, which produces a
   large diff. Prefer the single file.

3. Update `kmap/controller/foo.py` to match — see below.

4. Verify with the `verify-app` skill. A `.ui` change is not proven by the
   test suite.

5. Commit the `.ui` and its generated `.py` **together**. They are one change;
   splitting them leaves a commit where the app is broken.

## Keeping the controller in step

The generated class exposes each widget as `self.<objectName>`. So an
`objectName` is a contract between the two files, and renaming one in Designer
breaks the controller with an `AttributeError` at construction — which, in
several places here, lands inside a bare `except:` and shows up as a window
that silently fails to open rather than as a traceback.

After any rename, check both directions:

```bash
grep -rn "old_object_name" kmap/
```

New widgets are wired in the controller's `_connect()`, and initialised in
`_setup()` — not in `__init__`, and not in the `.ui`. Follow
`docs/development-guide.txt`; it is the author's own description of the
pattern.

Two rules from that guide worth repeating, because both cause real bugs:

- **No lambdas in `connect()`.** They keep the object alive and leak. Define
  your own signal and emit it instead.
- **Do not connect to another feature's widgets directly.** Connect to that
  feature's own signal.

## Promoted widgets

Several `.ui` files promote a plain `QWidget` to a kMap class (Designer's
*Promote to…*). The promotion appears in the XML as a `<customwidget>` entry
and turns into an import in the generated `.py`.

Promotion cannot pass constructor arguments, which is why a few controllers
build their children in code instead. If a widget needs arguments, it cannot
be promoted — do not try to work around that in the `.ui`.

Promoted classes are also why `make package` needs its `--hidden-import`
flags: PyInstaller cannot see an import that only exists inside generated UI
code. Adding a newly promoted widget means adding it to the `package` target
in the `Makefile`.

## A new window

1. Author `kmap/ui/foo.ui` in Designer; give every widget a descriptive
   `objectName` and group related controls in a `QGroupBox`.
2. Generate `kmap/ui/foo.py`.
3. Write `kmap/controller/foo.py` following the template in
   `docs/development-guide.txt`: `class Foo(QMainWindow, Foo_UI)`, then
   `setupUi(self)`, `_setup()`, `_connect()`.
4. If it holds or computes real data, put that in a `kmap/model/foo_model.py`
   with no Qt in it.
5. If it is opened from `MainWindow`, keep a reference in `self.sub_windows`
   or it will be garbage-collected the moment it appears.
