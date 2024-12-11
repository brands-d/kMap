import re


class Database:
    def __init__(self, path):
        self.molecules = []
        self.URL = ""

        self._load_molecules(path)

    def get_molecule_by_ID(self, ID):
        for molecule in self.molecules:
            if molecule.ID == ID:
                return molecule

        return None

    def _load_molecules(self, path):
        with open(path, "r") as file:
            first_line = file.readline()
            self.URL = first_line.split("=")[1][:-1]

            lines = []
            lines.append(file.readline())

            # Loop over all Molecules
            for line in file:
                if line[:11] == "moleculeID=":
                    new_molecule = Molecule(lines, URL=self.URL)
                    self.molecules.append(new_molecule)

                    lines = []

                lines.append(line)

            # Append last molecule
            new_molecule = Molecule(lines, URL=self.URL)
            self.molecules.append(new_molecule)


class Molecule:
    def __init__(self, lines, URL=""):
        self.ID = int(lines[0].split("=")[1])
        self.URL = URL + lines[2].split("=")[2][:-1]
        match = re.match(
            "^ShortName=(.*?), FullName=(.*?), Formula=(.*?), Orientation=(.*?), Charge=(.*?), MagneticMoment=(.*?), IP=(.*?), EA=(.*?), BasisSet=(.*?), XC-functional=(.*?)$",
            lines[1],
            re.MULTILINE,
        )
        self.short_name = match.group(1)
        self.full_name = match.group(2)
        self.formula = match.group(3)
        self.orientation = match.group(4)
        self.charge = int(match.group(5))
        self.magnetic_moment = float(match.group(6))
        self.IP = float(match.group(7))
        self.EA = float(match.group(8))
        self.basis_set = match.group(9)
        self.XC_functional = match.group(10)

        self.orbitals = []
        for index, line in enumerate(lines[3:], 1):
            new_orbital = Orbital(
                index, self.ID, line, self.URL, self.orientation, self.short_name
            )
            self.orbitals.append(new_orbital)

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


class Orbital:
    def __init__(self, ID, molecule_ID, line, URL="", orientation="xy", shortname=""):
        self.ID = ID
        self.database_ID = "%i.%i" % (molecule_ID, ID)
        match = re.match(
            "^CubeName=(.*?), OrbitalName=(.*?), OrbitalEnergy=(.*?), Occupation=(.*?), Symmetry=(.*?)$",
            line,
            re.MULTILINE,
        )
        self.URL = URL + match.group(1)
        self.name = shortname + " " + match.group(2)
        self.energy = float(match.group(3))
        self.occupation = int(match.group(4))
        self.symmetry = match.group(5)
        self.orientation = orientation

    def to_string(self):
        url = "URL: %s\n" % self.URL
        database_ID = "Database ID: %s" % self.database_ID
        name = "Name: %s\n" % self.name
        energy = "Energy: %.3f\n" % self.energy
        occupation = "Occupation: %i\n" % self.occupation
        symmetry = "Symmetry: %s" % self.symmetry

        return url + name + energy + occupation + symmetry

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
