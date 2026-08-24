# Issues

Problems found and deliberately not fixed. Delete an entry in the commit that
fixes it.

- **`test_application.py` tests nothing.** Its only test calls `kMap.test()`,
  which is `pass`. The Qt layer has no coverage at all; this file makes it
  look like it has some.

- **Bare `except:` hides download failures.**
  `OrbitalData.init_from_online` and `SlicedData.load_orbital_online` wrap the
  legacy h5serv attempt in a bare `except:`, so every error — including
  programming errors in the block — falls through to the cube path silently.

- **The h5serv path is probably dead.** `misc.get_remote_hdf5_orbital` and
  `Orbital.init_from_remote_hdf5` talk to `143.50.187.12:80`. Left in place
  pending confirmation that the host is gone.

- **`Config.set_key` is a public no-op.** It takes a value and does nothing.
  Either implement it or remove it.

- **The Bohr/Ångström constant exists three times.** `0.529177105787531` is
  written out in `Orbital._read_cube`, in `misc.write_cube` and in
  `library/database.py`. It should live in one place, but moving it touches
  the physics file and wants its own commit.

- **The database browser has no search across orbitals.** `find()` searches
  the tree, and orbitals are only in the tree once their molecule has been
  expanded, so a search only ever matches molecule names. That matches the
  field's own label, but the old eager tree could match orbitals too.
