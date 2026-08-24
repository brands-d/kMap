# kMap.py documentation

Topic guides for maintaining and extending the program. Start with
[architecture.md](architecture.md) for the big picture, then jump to whichever
topic you need.

| File | Covers |
|---|---|
| [architecture.md](architecture.md) | What the program is made of, and how a k-map gets on screen |
| [physics.md](physics.md) | The calculation itself: pipeline, units, conventions, parameters |
| [conventions.md](conventions.md) | Gotchas and rules that aren't obvious from the code alone |
| [testing.md](testing.md) | What the tests cover, what they don't, and how to run them |
| [cheatsheet.md](cheatsheet.md) | Every command you'll actually type, with no surrounding prose |
| [development-guide.txt](development-guide.txt) | The author's own guide to adding a feature (controller / model / `.ui`) |
| [Sliced Data Description.txt](Sliced%20Data%20Description.txt) | The `.hdf5` layout `SlicedData` reads and writes |

`classes_kMap.png` and `packages_kMap.png` are `pyreverse` output
(`make generate-uml`) and go stale; trust the code over them.
`styleguide/` is an offline copy of PEP 8.

Two short files live at the repo root rather than here, because they change
with the work rather than describing the program:

| File | Covers |
|---|---|
| [../ISSUES.md](../ISSUES.md) | Known problems, deliberately not fixed yet |
| [../NOTES.md](../NOTES.md) | Facts a later session needs and cannot read off the code |
