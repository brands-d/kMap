"""Defines the Database class.

This file defines the classes representing the online orbital database
hosted at physikmdb.uni-graz.at, and the loading of a single orbital from
it. The database serves the coefficients of an LCAO-GTO expansion instead
of finished cube files, so the real space orbital is evaluated locally by
the physikmdb package.
"""

import logging
import re
import tempfile
from pathlib import Path

import numpy as np
import physikmdb

from kmap.config.config import config

# Conversion factor from Bohr to Angstroem
b2a = 0.529177105787531

# Number of orbitals listed above and below the HOMO. A calculation holds
# every orbital it computed, which is far more than is ever of interest.
orbital_window = 20

# Locator the database windows hand down to the loading code.
url_pattern = re.compile(r"^physikmdb://(\d+)/(\d+)$")

# URLs of the old site, kept working so that projects saved before the
# switch can still find their orbitals. The number is the moleculeID of
# the old database, which the new one stores as "legacy_id".
legacy_url_pattern = re.compile(r"cubefiles/(\d+)/.*_MO_(\d+)$")


def connect(url=None):
    """Returns a client for the online database.

    The download cache is kept per instance. The physikmdb package keys its
    own cache by the calculation's storage folder alone, so two instances
    numbering their calculations the same way silently share files.

    Args:
        url (str): Address of the instance. Defaults to the settings.

    Returns:
        (physikmdb.Database): The client.
    """

    if url is None:
        url = config.get_key("database", "url")

    cache_dir = (
        Path(tempfile.gettempdir()) / "kmap-database-cache" / re.sub(r"\W+", "_", url)
    )

    return physikmdb.Database(url, cache_dir=cache_dir)


class Database:
    def __init__(self, url=None):
        self.URL = config.get_key("database", "url") if url is None else url
        self.molecules = []

        self._database = connect(self.URL)

        self._load_molecules()

    def get_molecule_by_ID(self, ID):
        for molecule in self.molecules:
            if molecule.ID == ID:
                return molecule

        return None

    def get_XC_functionals(self):
        """Returns all XC-functionals the database offers as filters."""

        return self._database.filters()["xc_functional"]

    def _load_molecules(self):
        # A calculation carries the basis set and the XC-functional, and is
        # therefore what the old database called a molecule. The name and
        # the formula belong to the system it was run on.
        systems = {system.id: system for system in self._database.systems()}
        calculations = self._database.calculations(calculation_type="groundstate")

        self.molecules = []
        for calculation in calculations:
            system = systems.get(calculation.system_id)

            if system is None:
                continue

            self.molecules.append(Molecule(calculation, system, self.URL))


class Molecule:
    def __init__(self, calculation, system, url=""):
        self.ID = calculation.id
        self.URL = "%s/%i" % (url.rstrip("/"), calculation.id)
        self.short_name = system.short_name
        self.full_name = system.full_name
        self.formula = system.formula
        self.orientation = calculation.raw.get("orientation", "xy")
        self.charge = int(calculation.charge or 0)
        # The old database listed the number of unpaired electrons, the new
        # one the total spin.
        self.magnetic_moment = 2 * float(calculation.spin or 0)
        # Koopmans' theorem, the same convention the old database used.
        self.IP = -(calculation.homo_energy or 0)
        self.EA = -(calculation.lumo_energy or 0)
        self.basis_set = calculation.basis_set
        self.XC_functional = calculation.xc_functional

        self._calculation = calculation
        self._orbitals = None

    @property
    def orbitals(self):
        """The frontier orbitals, downloaded on first use."""

        if self._orbitals is None:
            self._orbitals = self._load_orbitals()

        return self._orbitals

    def to_string(self):
        ID = "ID: %i\n" % self.ID
        URL = "URL: %s\n" % self.URL
        small_name = "Short Name: % s\n" % self.short_name
        full_name = "Full Name: %s\n" % self.full_name
        formula = "Formula: %s\n" % self.formula
        orientation = "Orientation: %s\n" % self.orientation
        charge = "Charge: %i\n" % self.charge
        magnetic_moment = "Magnetic Moment: %.3f\n" % self.magnetic_moment
        IP = "IP: %.2f\n" % self.IP
        EA = "EA: %.2f\n" % self.EA
        basis_set = "Basis Set: %s\n" % self.basis_set
        XC_functional = "XC-Functional: %s\n" % self.XC_functional
        length = "Number of Orbitals: %i" % len(self.orbitals)

        return (
            ID
            + URL
            + small_name
            + full_name
            + formula
            + orientation
            + charge
            + magnetic_moment
            + IP
            + EA
            + basis_set
            + XC_functional
            + length
        )

    def _load_orbitals(self):
        log = logging.getLogger("kmap")
        log.info("Loading orbitals of calculation %i..." % self.ID)

        orbitals = self._calculation.orbitals
        centre = self._get_HOMO_position(orbitals)
        first = max(centre - orbital_window, 0)
        last = centre + orbital_window + 1

        return [Orbital(orbital, self) for orbital in orbitals[first:last]]

    def _get_HOMO_position(self, orbitals):
        # Position in the list, not the index in the coefficient file: for
        # an unrestricted calculation the two spin channels share the list.
        for position, orbital in enumerate(reversed(orbitals)):
            if orbital.occupation:
                return len(orbitals) - position - 1

        return len(orbitals) // 2


class Orbital:
    def __init__(self, orbital, molecule):
        self.ID = orbital.index + 1
        self.database_ID = "%i.%i" % (molecule.ID, self.ID)
        self.URL = "physikmdb://%i/%i" % (molecule.ID, orbital.index)
        self.name = "%s %s" % (molecule.short_name, orbital.name)
        self.energy = 0.0 if orbital.energy is None else orbital.energy
        self.occupation = int(orbital.occupation or 0)
        self.symmetry = "" if orbital.symmetry is None else orbital.symmetry
        self.orientation = molecule.orientation

        if orbital.spin is not None:
            self.name += " (%s)" % orbital.spin

    def to_string(self):
        url = "URL: %s\n" % self.URL
        database_ID = "Database ID: %s\n" % self.database_ID
        name = "Name: %s\n" % self.name
        energy = "Energy: %.3f\n" % self.energy
        occupation = "Occupation: %i\n" % self.occupation
        symmetry = "Symmetry: %s" % self.symmetry

        return url + database_ID + name + energy + occupation + symmetry

    def get_meta_data(self):
        meta_data = {
            "name": self.name,
            "ID": self.ID,
            "database ID": self.database_ID,
            "energy": self.energy,
            "occupation": self.occupation,
            "symmetry": self.symmetry,
            "orientation": self.orientation,
        }

        return meta_data


def is_database_url(url):
    """Whether this URL denotes an orbital of the online database."""

    return bool(url_pattern.match(url) or legacy_url_pattern.search(url))


def cache_name(url):
    """Returns the file name an orbital downloaded from url is cached as."""

    match = url_pattern.match(url)
    if match:
        return "physikmdb_%s_%s" % (match.group(1), match.group(2))

    if "cubefiles/" in url:
        return url.split("cubefiles/")[1].replace("/", "_")

    return url.rstrip("/").split("/")[-1]


def load_orbital(url):
    """Evaluates one orbital of the online database on a real space grid.

    The database holds the coefficients of an LCAO-GTO expansion, not a
    cube file, so the orbital is computed here. The grid is a cube centred
    on the origin, large enough to hold the molecule plus the padding set
    in the settings.

    Args:
        url (str): Locator of the orbital, as handed out by the database
            windows.

    Returns:
        (tuple): The psi and molecule dictionaries the Orbital class takes
            for the "psi" file format.
    """

    log = logging.getLogger("kmap")
    calculation_ID, index = _parse_url(url)

    spacing = float(config.get_key("orbital", "grid_spacing"))
    padding = float(config.get_key("orbital", "grid_padding"))

    calculation = connect().calculation(calculation_ID)
    basis = calculation.basis

    coordinates = (
        np.stack([basis.Rx, basis.Ry, basis.Rz], axis=1).astype("float64") * b2a
    )
    # The grid is centred on the origin, as the Orbital class expects, so it
    # has to reach the atom furthest from it in any direction.
    extent = np.abs(coordinates).max() + padding
    num = int(2 * extent / spacing) + 1

    log.info(
        "Computing orbital %i of calculation %i on a %i^3 grid..."
        % (index, calculation_ID, num)
    )
    data = _evaluate(calculation, index, extent, num)

    grid = np.linspace(-extent, +extent, num)
    step = grid[1] - grid[0]
    psi = {
        "name": "%s_MO_%i" % (calculation.name, index + 1),
        "nx": num,
        "ny": num,
        "nz": num,
        "dx": step,
        "dy": step,
        "dz": step,
        "x": grid,
        "y": grid,
        "z": grid,
        "data": data,
    }
    molecule = {
        "num_atom": basis.n_atoms,
        "chemical_numbers": [int(number) for number in basis.atomic_numbers],
        "atomic_coordinates": coordinates,
    }

    return psi, molecule


def _evaluate(calculation, index, extent, num):
    # physikmdb writes x fastest and therefore returns [iz, iy, ix], while
    # everything here expects [ix, iy, iz] the way a cube file is written.
    data = calculation.wavefunction(index, extent=extent, points=num)

    return np.ascontiguousarray(data.transpose(2, 1, 0), dtype="float64")


def _parse_url(url):
    match = url_pattern.match(url)
    if match:
        return int(match.group(1)), int(match.group(2))

    match = legacy_url_pattern.search(url)
    if match:
        return _resolve_legacy_url(int(match.group(1)), int(match.group(2)))

    raise ValueError("'%s' is not a database orbital." % url)


def _resolve_legacy_url(legacy_ID, orbital_number):
    log = logging.getLogger("kmap")
    log.info("Resolving old database URL for molecule %i..." % legacy_ID)

    for calculation in connect().calculations(calculation_type="groundstate"):
        if calculation.raw.get("legacy_id") == legacy_ID:
            return calculation.id, orbital_number - 1

    raise ValueError("Molecule %i of the old database is gone." % legacy_ID)
