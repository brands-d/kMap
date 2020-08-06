class Database():

    def __init__(self, path):

        self.molecules = []
        self.URL = ''

        self._load_molecules(path)

    def get_molecule_by_ID(self, ID):

        for molecule in self.molecules:
            if molecule.ID == ID:
                return molecule

        return None

    def _load_molecules(self, path):

        with open(path, 'r') as file:

            first_line = file.readline()
            self.URL = first_line.split('=')[1][:-1]

            lines = []
            lines.append(file.readline())

            # Loop over all Molecules
            for line in file:
                if line[:11] == 'moleculeID=':
                    new_molecule = Molecule(lines)
                    self.molecules.append(new_molecule)

                    lines = []

                lines.append(line)


class Molecule():

    def __init__(self, lines):

        self.ID = int(lines[0].split('=')[1])
        self.URL = lines[2].split('=')[2][:-1]

        parts = lines[1].split(',')

        self.short_name = parts[0].split('=')[1]
        self.full_name = parts[1].split('=')[1]
        self.charge = int(parts[2].split('=')[1])
        self.magnetic_moment = float(parts[3].split('=')[1])
        self.XC_functional = parts[4].split('=')[1]

        self.orbitals = []
        for line in lines[3:]:
            new_orbital = Orbital(line)
            self.orbitals.append(new_orbital)

    def to_string(self):

        id_ = 'ID: %i\n' % self.ID
        url = 'URL: %s\n' % self.URL
        sn = 'Short Name: % s\n' % self.short_name
        fn = 'Full Name: %s\n' % self.full_name
        charge = 'Charge: %i\n' % self.charge
        mag = 'Magnetic Moment: %.5f\n' % self.magnetic_moment
        cxf = 'XC-Functional: %s\n' % self.XC_functional
        length = 'Number of Orbitals: %i' % len(self.orbitals)

        return id_ + url + sn + fn + charge + mag + cxf + length


class Orbital():

    def __init__(self, line):

        parts = line.split(',')
        self.URL = parts[0].split('=')[1]
        self.name = parts[1].split('=')[1]
        self.energy = float(parts[2].split('=')[1])
        self.occupation = int(parts[3].split('=')[1])
        self.symmetry = parts[4].split('=')[1][:-1]

    def to_string(self):

        url = 'URL: %s\n' % self.URL
        name = 'Name: % s\n' % self.name
        energy = 'Energy: %.5f\n' % self.energy
        occ = 'Occupation: %i\n' % self.occupation
        sym = 'Symmetry: %s' % self.symmetry

        return url + name + energy + occ + sym
