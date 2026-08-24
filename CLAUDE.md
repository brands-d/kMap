# CLAUDE.md

Orientation for Claude Code sessions in this repo. Pointers and rules — for
project knowledge read [`docs/`](docs/README.md).

## The one thing that matters most

**kMap.py's current output is the ground truth.** The code is amateur work in
places and it shows, but the physics has been used and checked by many people
in many situations over years, and a professor contributed the parts that
matter most. A refactor that produces a slightly different momentum map has
not improved anything — it has broken the program, silently, in the one way
nobody will file a bug for.

So: **change the numbers only when you can show the old ones were wrong.**
Never on the grounds that the new way is cleaner. When you touch
`kmap/library/orbital.py`, the 3D-FT, the hemisphere cut, the |A·k|² factors,
the symmetrization, or any unit conversion, prove the output is unchanged with
the `physics-check` skill before saying it works.

Everything else — structure, naming, UI, dependencies — is fair game and much
of it needs the work.

## Who this is for

Written years ago by one person learning as he went, and only barely
maintained since: obvious design flaws, UI/UX problems, install and dependency
pain, inconsistent documentation, and feature creep. It is used for real
research anyway, mostly at Uni Graz, and it is the only tool for some of what
it does.

That history is the reason for the rule above and not an excuse to rewrite.
The plan is to fix the flaws deliberately, one reviewable change at a time.

## Match the existing style

The code has a style. It is not the style you would pick, and it is still the
one to write in. A file where half the functions are annotated and the other
half are not is worse than either.

- No type hints. No `dataclass`. Plain classes with plain `__init__`.
- Formatted with **black** defaults (double quotes, trailing commas, 88 cols).
- `"%s" % value` and f-strings both appear; prefer whatever the surrounding
  file already uses.
- GUI features follow the controller / model / `.ui` pattern, including the
  `_setup()` and `_connect()` methods. `docs/development-guide.txt` is the
  author's own description of it — read it before adding a feature.
- Docstrings are Google-style with an `Args:` block, and only on the classes
  and methods that carry real logic. Most methods have none. Do not add them
  everywhere as a side errand.
- `ID` and `URL` are spelled in caps, because they are everywhere else.

Do not introduce a formatter, linter, type checker, `pyproject.toml`, or test
framework as a side effect of another task. If one of those is worth adding,
it is worth its own conversation.

## Start here

- [`docs/architecture.md`](docs/architecture.md) — what the program is made of
- [`docs/physics.md`](docs/physics.md) — the calculation, its units and conventions
- [`docs/conventions.md`](docs/conventions.md) — non-obvious gotchas
- [`docs/cheatsheet.md`](docs/cheatsheet.md) — every command you'll need
- [`docs/testing.md`](docs/testing.md) — what the tests cover, and what they don't
- [`ISSUES.md`](ISSUES.md) / [`NOTES.md`](NOTES.md) — read both before starting

## Rules

1. **Ask rather than assume.** If a question could change what you build, ask
   it. Two readings of the code, an ambiguous requirement, a judgement call
   about scope — all worth a question. A wrong guess in a physics program
   produces pictures that look fine and are wrong.
2. **Never edit `kmap/ui/*.py`.** Those files are generated from the `.ui`
   files by `pyside6-uic`. Edit the `.ui` and regenerate. See the `ui-change`
   skill.
3. **Never edit `*_default.ini`'s meaning without saying so.** Users' settings
   live in `*_user.ini` and override the defaults key by key. A renamed key
   silently drops a user's setting. The `_user` files are gitignored.
4. **Don't break saved projects.** `.kmap` files are `bz2` + `pickle` of live
   objects. Renaming or removing an attribute on a class that ends up in a
   save makes old projects unloadable. Check `save_state`/`restore_state`
   before touching one.
5. **Commit in small batches.** One logical change per commit, reviewable and
   revertable alone.
6. **Leave a worktree committed.** Finishing or pausing work in a worktree
   means a clean `git status`.
7. **Keep `ISSUES.md` and `NOTES.md` current.** See below.

## Testing while you work

```
python -m unittest kmap.tests.test_orbital     # one file, while editing
python -m unittest discover                    # all of it, ~6 s
```

There is no faster tier and no coverage tooling. 59 tests, weighted heavily
towards `library/`; the Qt layer is nearly untested, so a GUI change is only
proven by running the app (`verify-app` skill).

Never commit on a red tree. If a test was already failing before you started,
say so rather than quietly matching it.

## Commit messages

Match the existing history: one short sentence, past tense, saying what was
done. No prefixes, no body unless there is something a reader genuinely
cannot get from the diff.

```
Fixed symmetrization bug.
Allowed orientation angles on the orbitaldatatab from -180 to 180
```

## ISSUES.md and NOTES.md

Two short files at the repo root, both tracked:

- **`ISSUES.md`** — problems found but deliberately not fixed, because they
  were out of scope. What is wrong, where, why it was skipped.
- **`NOTES.md`** — facts a later session needs and cannot get from the code:
  a measured result, a rejected approach and why, a constraint learned the
  hard way.

Rules for both, and they matter more than the content:

- **Keep them short.** A long file is an unread file.
- **Delete on resolution.** Fixing an issue removes its entry in the same
  commit.
- **Ask before adding or removing an entry** unless the user already said to
  record it. These are the user's files, not a scratchpad.
- Do not restate what the code, the docs or git history already say.

## Writing style

Write for a competent maintainer who can read Python and knows photoemission.
Do not explain the physics, and do not narrate how the code got this way —
that belongs in the commit message.

Comments: default to none. Reach for one when the code genuinely cannot say
it — a unit, a non-obvious constraint, a deliberate choice that looks like a
mistake. Then write one line.

The existing code is *under*-commented in the physics and over-commented in
the plumbing. Fixing that is its own pass, not a side errand.

## Things that will bite you

- The virtual environment lives in the **main checkout**, not in a worktree:
  `/Users/dominik/lib/kMap/.venv`. Worktrees share it.
- `kmap/ui/*.py` are generated. See rule 2.
- Cube files are read in **Bohr** and immediately converted to **Ångström**
  (`b2a = 0.529177105787531`). Everything above `_read_cube` is Å and eV.
  `kmap/library/orbital.py` is the only place that conversion happens.
- Since 2022-08-08 `_read_cube` re-centres the box on the origin and shifts
  the atoms with it. The cube file's own origin is discarded. A change here
  moves every atom relative to every orbital.
- `Orbital` caches aggressively (`self.kmap`, `self.Ak`) and only recomputes
  when its `check_new_*` methods say a parameter changed. Add a parameter
  without adding it to the matching `check_new_*` and the display silently
  keeps showing the old result.
- `paths.cache` defaults to `None`, meaning caching is **off**. Downloaded
  and computed orbitals are recomputed every session unless the user sets it.
- pyqtgraph's `imageAxisOrder` is set from the config at startup. Array
  indexing conventions in the plotting layer depend on it.

## Skills

Invoke these rather than improvising:

- `physics-check` — validate anything touching orbitals, k-maps or units
- `verify-app` — prove a GUI change works in the running application
- `ui-change` — the `.ui` / `pyside6-uic` loop
