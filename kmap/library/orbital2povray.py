from configparser import ConfigParser

import numpy as np
from skimage import measure

number2symbol = {
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    21: "Sc",
    22: "Ti",
    23: "V",
    24: "Cr",
    25: "Mn",
    26: "Fe",
    27: "Co",
    28: "Ni",
    29: "Cu",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    39: "Y",
    40: "Zr",
    41: "Nb",
    42: "Mo",
    43: "Tc",
    44: "Ru",
    45: "Rh",
    46: "Pd",
    47: "Ag",
    48: "Cd",
    49: "In",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
    54: "Xe",
    55: "Cs",
    56: "Ba",
    57: "La",
    58: "Ce",
    59: "Pr",
    60: "Nd",
    61: "Pm",
    62: "Sm",
    63: "Eu",
    64: "Gd",
    65: "Tb",
    66: "Dy",
    67: "Ho",
    68: "Er",
    69: "Tm",
    70: "Yb",
    71: "Lu",
    72: "Hf",
    73: "Ta",
    74: "W",
    75: "Re",
    76: "Os",
    77: "Ir",
    78: "Pt",
    79: "Au",
    80: "Hg",
    81: "Tl",
    82: "Pb",
    83: "Bi",
    84: "Po",
    85: "At",
    86: "Rn",
    87: "Fr",
    88: "Ra",
    89: "Ac",
    90: "Th",
    91: "Pa",
    92: "U",
    93: "Np",
    94: "Pu",
    95: "Am",
    96: "Cm",
    97: "Bk",
    98: "Cf",
    99: "Es",
    100: "Fm",
}


class Orbital2Povray:
    """
    This file defines a class named Orbital2Povray designed to convert
    3D orbital-data from the Orbital class into povray format for rendering
    the molecular backbone as well as isosurface of the 3D data
    either in real space or in reciprocal space

    Args:
        data (3D numpy-array): 3D data cube used for plotting isosurfaces
        grid (dict): keys 'nx', 'ny', 'nz', 'dx', 'dy', 'dz' define grid for data
        structure (dict): chemiical elements and positions of atoms in structure
        settings (str): path to POV-ray settings file

    Public Methods:
        get_bonds(lower_factor=0.8, upper_factor=1.2):
        get_isosurface(isoval):
        get_isocolor(index):
        write_povfile(filename):
        run_povray(executable)

    Private Methods:
        _write_atoms(self, file):
        _write_bonds(self, file):
        _write_isosurface(self, file, isovalue, vertices, faces, color):
        _get_atomsetting(self, element):
        _write_header(self, file):
        _write_macros(self, file):

    Attributes:
        domain (str): either 'real' or 'reciprocal' for real or momentum space isosurface
        data (3D numpy-array): 3D data cube used to compute isosurface
        grid (dict): keys, nx, ny, nz, dx, dy, dz specifying data grid
        structure (dict): contains chemical elements and atomic positions of molecule
        bonds (list): list of atom indices for bond connectivity
        settings (ConfigParser): settings used in povray input file
        isovalues (list): list of floats specifying the values for the isosurface(s)
        pov_file (str): filename of povray file

    """

    def __init__(self, data, grid, structure, settingsfile):
        self.data = data
        self.colordata = None  # optional 3D-array for coloring isosurface
        self.grid = grid
        self.structure = structure

        if structure != None:
            self.get_bonds()

        self.settingsfile = settingsfile
        self.settings = ConfigParser()
        self.settings.read(settingsfile)
        self.local_settings = {}

        if len(data) != 0:
            self.isovalues = self.settings["isosurface"]["isovalues"]
            self.get_isosurface()

    @classmethod
    def init_from_cube(
        cls,
        cubefile,
        domain,
        settingsfile,
        dk3D=0.15,
        E_kin_max=150,
        value="abs2",
        isosurface=True,
        structure=True,
    ):
        from kmap.library.orbital import Orbital

        # Orbital object contains molecular geometry and psi(x,y,z)
        orbital = Orbital(cubefile, dk3D=dk3D, E_kin_max=E_kin_max, value=value)

        if domain == "real":
            if isosurface:
                data = orbital.psi["data"]
                grid = {
                    "origin": [
                        orbital.psi["x"][0],
                        orbital.psi["y"][0],
                        orbital.psi["z"][0],
                    ],
                    "nx": orbital.psi["nx"],
                    "ny": orbital.psi["ny"],
                    "nz": orbital.psi["nz"],
                    "a": [orbital.psi["x"][-1] - orbital.psi["x"][0], 0, 0],
                    "b": [0, orbital.psi["y"][-1] - orbital.psi["y"][0], 0],
                    "c": [0, 0, orbital.psi["z"][-1] - orbital.psi["z"][0]],
                }
            else:
                data, grid = [], {}

            if structure:
                structure = orbital.molecule

            else:
                structure = None

        elif domain == "reciprocal":
            if isosurface:
                data = orbital.psik["data"]
                grid = {
                    "origin": [
                        orbital.psik["kx"][0],
                        orbital.psik["ky"][0],
                        orbital.psik["kz"][0],
                    ],
                    "nx": orbital.psik["data"].shape[0],
                    "ny": orbital.psik["data"].shape[1],
                    "nz": orbital.psik["data"].shape[2],
                    "a": [orbital.psik["kx"][-1] - orbital.psik["kx"][0], 0, 0],
                    "b": [0, orbital.psik["ky"][-1] - orbital.psik["ky"][0], 0],
                    "c": [0, 0, orbital.psik["kz"][-1] - orbital.psik["kz"][0]],
                }
            else:
                data, grid = [], {}

            structure = None

        return cls(data, grid, structure, settingsfile)

    @classmethod
    def init_from_vasp(cls, poscar_file, settingsfile, isosurface=False):
        from poscar import Poscar

        pos = Poscar(poscar_file)
        structure = pos.unitcell

        if isosurface:
            data, grid = pos.get_data()

        else:
            data, grid = [], {}

        return cls(data, grid, structure, settingsfile)

    def copy(self):
        # make an independent copy of the whole object

        data = self.data[:]

        grid = {}
        for key in self.grid:
            if type(self.grid[key]) != int:
                grid[key] = self.grid[key].copy()
            else:
                grid[key] = self.grid[key]

        structure = {}
        for key in self.structure:
            if key != "num_atom":
                structure[key] = self.structure[key].copy()
            else:
                structure[key] = self.structure[key]

        settingsfile = self.settingsfile

        return Orbital2Povray(data, grid, structure, settingsfile)

    def expand_structure(self, boundary):
        from math import ceil, floor

        base = self.structure["internal_coordinates"]
        base -= base > 1.0
        base += base < 0.0
        Z_list = self.structure["chemical_numbers"]
        num_base = len(Z_list)

        # add unit cells
        imin, imax = floor(boundary["a"][0]), ceil(boundary["a"][1])
        jmin, jmax = floor(boundary["b"][0]), ceil(boundary["b"][1])
        kmin, kmax = floor(boundary["c"][0]), ceil(boundary["c"][1])
        num_cells = (imax - imin) * (jmax - jmin) * (kmax - kmin)
        num_atoms = num_cells * len(Z_list)
        internal = np.zeros((num_atoms, 3))
        elements = np.zeros((num_atoms), dtype=int)
        count = 0
        for i in range(imin, imax):
            for j in range(jmin, jmax):
                for k in range(kmin, kmax):
                    indices = range((count * num_base), ((count + 1) * num_base))
                    internal[indices, 0] = base[:, 0] + i
                    internal[indices, 1] = base[:, 1] + j
                    internal[indices, 2] = base[:, 2] + k
                    elements[indices] = Z_list
                    count += 1

        # cut out atoms according to boundaries w.r.t. internal coordiantes
        for i, ax in enumerate(["a", "b", "c"]):
            cmin, cmax = boundary[ax][0], boundary[ax][1]
            keep_atoms = np.logical_and(
                internal[:, i] >= cmin, internal[:, i] <= cmax
            ).nonzero()[0]
            internal = np.take(internal, keep_atoms, axis=0)
            elements = np.take(elements, keep_atoms)

        # cut out atoms according to boundaries w.r.t. cartesian coordiantes
        cartesian = self.internal_to_cartesian(internal)
        for i, ax in enumerate(["x", "y", "z"]):
            if boundary[ax] != []:
                cmin, cmax = boundary[ax][0], boundary[ax][1]
                keep_atoms = np.logical_and(
                    cartesian[:, i] >= cmin, cartesian[:, i] <= cmax
                ).nonzero()[0]
                cartesian = np.take(cartesian, keep_atoms, axis=0)
                elements = np.take(elements, keep_atoms)

        self.structure["atomic_coordinates"] = cartesian
        self.structure["chemical_numbers"] = elements
        self.get_bonds()

        return

    def expand_isosurface(self, boundary, method="puzzle", memory_limit="4 GByte"):
        if method == "puzzle":
            expanded_surfaces = self.isosurface_puzzle(boundary)

        elif method == "seamless":
            expanded_surfaces = self.isosurface_seamless(boundary, memory_limit)

        self.isosurface = expanded_surfaces

    def get_bonds(self, lower_factor=0.7, upper_factor=1.2):
        """returns a list of bonds as list of atom indices

        Args:
            lower_factor (float): lower bound for drawing bonds w.r.t sum of covalent radii
            upper_factor (float): upper bound for drawing bonds w.r.t sum of covalent radii
        """
        covalent_R = {
            1: 0.32,
            2: 0.32,  # H, He
            3: 1.34,
            4: 0.90,
            5: 0.82,
            6: 0.77,
            7: 0.71,
            8: 0.73,
            9: 0.71,
            10: 0.69,  # Li - Ne
            11: 1.54,
            12: 1.30,
            13: 1.18,
            14: 1.11,
            15: 1.06,
            16: 1.02,
            17: 0.99,
            18: 0.97,  # Na- Ar
            19: 1.96,
            20: 1.74,
            21: 1.44,
            22: 1.36,
            23: 1.25,
            24: 1.27,
            25: 1.39,
            26: 1.25,  # K - Fe
            27: 1.26,
            28: 1.21,
            29: 1.38,
            30: 1.31,
            31: 1.26,
            32: 1.22,
            33: 1.21,
            34: 1.16,  # Co- Se
            35: 1.14,
            36: 1.10,  # Br, Kr
            37: 2.11,
            38: 1.92,
            39: 1.62,
            40: 1.48,
            41: 1.37,
            41: 1.45,
            43: 1.31,
            44: 1.26,  # Rb -Ru
            45: 1.35,
            46: 1.31,
            47: 1.53,
            48: 1.48,
            49: 1.44,
            50: 1.41,
            51: 1.38,
            52: 1.35,  # Rh -Te
            53: 1.33,
            54: 1.30,  # I, Xe
            55: 2.25,
            56: 1.98,
            57: 1.69,
            72: 1.50,
            73: 1.38,
            74: 1.46,
            75: 1.59,
            76: 1.28,  # Cs -Os
            77: 1.37,
            78: 1.38,
            79: 1.38,
            80: 1.49,
            81: 1.48,
            82: 1.46,
            83: 1.46,
            84: 1.40,  # Ir -Po
            85: 1.45,
            86: 1.45,
        }  # At, Rn

        coordinates = self.structure["atomic_coordinates"]
        Z_list = self.structure["chemical_numbers"]
        bonds = []
        for i in range(len(Z_list)):
            x1, y1, z1 = coordinates[i][0], coordinates[i][1], coordinates[i][2]
            R1 = covalent_R[Z_list[i]]
            for j in range(i + 1, len(Z_list)):
                x2, y2, z2 = coordinates[j][0], coordinates[j][1], coordinates[j][2]
                R2 = covalent_R[Z_list[j]]
                R = R1 + R2  # sum of covalent radii
                distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
                #                if Z_list[i] == 22 and Z_list[j] ==8:
                #                    print('Ti-O: ', R1, R2, R1+R2, distance)
                if lower_factor * R <= distance <= upper_factor * R:
                    bonds.append([i, j])

        self.bonds = bonds

        return

    def get_isosurface(self, isovalues=None, colors=None):
        if isovalues is None:
            isovalues = self.isovalues.split(",")

        if colors is None:
            colors = []
            for i in range(len(isovalues)):
                colors.append(self.get_isocolor(i))

        self.isosurface = []
        for i in range(len(isovalues)):
            isovalue = float(isovalues[i])
            iso = isovalue * self.data.max()

            if self.data.min() <= iso <= self.data.max():
                # get vertices (v_) and faces (f) or triangularized isosurface
                # v_, f = pg.isosurface(self.data, iso)
                v_, f, normals, values = measure.marching_cubes(self.data, iso)

                # scale and shift vertices according to the (possibly non-orthogonal) unit cell vectors
                v = np.zeros_like(v_)
                a, b, c = self.grid["a"], self.grid["b"], self.grid["c"]
                nx, ny, nz = self.grid["nx"], self.grid["ny"], self.grid["nz"]
                origin = self.grid["origin"]
                v[:, 0] = v_[:, 0] / (nx - 1)
                v[:, 1] = v_[:, 1] / (ny - 1)
                v[:, 2] = v_[:, 2] / (nz - 1)
                v[:, 0] = origin[0] + v[:, 0] * a[0] + v[:, 1] * b[0] + v[:, 2] * c[0]
                v[:, 1] = origin[1] + v[:, 0] * a[1] + v[:, 1] * b[1] + v[:, 2] * c[1]
                v[:, 2] = origin[2] + v[:, 0] * a[2] + v[:, 1] * b[2] + v[:, 2] * c[2]

                color = colors[i]

                if len(v) > 3:
                    self.isosurface.append(
                        {
                            "isovalue": isovalue,
                            "color": color,
                            "vertices": v,
                            "faces": f,
                            "normals": normals,
                        }
                    )

        return

    def isosurface_puzzle(self, boundary):
        # check how many unit cells are needed
        from math import ceil, floor

        imin, imax = floor(boundary["a"][0]), ceil(boundary["a"][1])
        jmin, jmax = floor(boundary["b"][0]), ceil(boundary["b"][1])
        kmin, kmax = floor(boundary["c"][0]), ceil(boundary["c"][1])
        num_cells = (imax - imin) * (jmax - jmin) * (kmax - kmin)

        # unit cell vectors
        a, b, c = self.grid["a"], self.grid["b"], self.grid["c"]
        nx, ny, nz = self.grid["nx"], self.grid["ny"], self.grid["nz"]
        a_grid = np.linspace(0, 1, nx, endpoint=False)
        b_grid = np.linspace(0, 1, ny, endpoint=False)
        c_grid = np.linspace(0, 1, nz, endpoint=False)
        A, B, C = np.meshgrid(a_grid, b_grid, c_grid, indexing="ij")

        surfaces = self.isosurface
        expanded_surfaces = []
        origin = [0, 0, 0]
        for surface in surfaces:
            isovalue = surface["isovalue"]
            iso = isovalue * self.data.max()
            color = surface["color"]

            for i in range(imin, imax):
                for j in range(jmin, jmax):
                    for k in range(kmin, kmax):
                        X = (A + i) * a[0] + (B + j) * b[0] + (C + k) * c[0]
                        Y = (A + i) * a[1] + (B + j) * b[1] + (C + k) * c[1]
                        Z = (A + i) * a[2] + (B + j) * b[2] + (C + k) * c[2]
                        inside = (X >= boundary["x"][0]) * (X <= boundary["x"][1])
                        inside *= (Y >= boundary["y"][0]) * (Y <= boundary["y"][1])
                        inside *= (Z >= boundary["z"][0]) * (Z <= boundary["z"][1])
                        if self.data[inside] != []:
                            if self.data[inside].min() < iso < self.data[inside].max():
                                v_, f, normals, values = measure.marching_cubes(
                                    self.data, iso, mask=inside
                                )
                                v = np.zeros_like(v_)

                                origin[0] = (
                                    self.grid["origin"][0]
                                    + i * a[0]
                                    + j * b[0]
                                    + k * c[0]
                                )
                                origin[1] = (
                                    self.grid["origin"][1]
                                    + i * a[1]
                                    + j * b[1]
                                    + k * c[1]
                                )
                                origin[2] = (
                                    self.grid["origin"][2]
                                    + i * a[2]
                                    + j * b[2]
                                    + k * c[2]
                                )
                                v_[:, 0] /= nx
                                v_[:, 1] /= ny
                                v_[:, 2] /= nz
                                v[:, 0] = (
                                    origin[0]
                                    + v_[:, 0] * a[0]
                                    + v_[:, 1] * b[0]
                                    + v_[:, 2] * c[0]
                                )
                                v[:, 1] = (
                                    origin[1]
                                    + v_[:, 0] * a[1]
                                    + v_[:, 1] * b[1]
                                    + v_[:, 2] * c[1]
                                )
                                v[:, 2] = (
                                    origin[2]
                                    + v_[:, 0] * a[2]
                                    + v_[:, 1] * b[2]
                                    + v_[:, 2] * c[2]
                                )

                                expanded_surfaces.append(
                                    {
                                        "isovalue": isovalue,
                                        "color": color,
                                        "vertices": v,
                                        "faces": f,
                                        "normals": normals,
                                    }
                                )
        return expanded_surfaces

    def isosurface_seamless(self, boundary, memory_limit):
        # check how many unit cells are needed
        from math import ceil, floor

        imin, imax = floor(boundary["a"][0]), ceil(boundary["a"][1])
        jmin, jmax = floor(boundary["b"][0]), ceil(boundary["b"][1])
        kmin, kmax = floor(boundary["c"][0]), ceil(boundary["c"][1])
        num_cells = (imax - imin) * (jmax - jmin) * (kmax - kmin)

        # unit cell vectors
        a, b, c = self.grid["a"], self.grid["b"], self.grid["c"]
        nx, ny, nz = self.grid["nx"], self.grid["ny"], self.grid["nz"]

        origin = [0, 0, 0]
        origin[0] = self.grid["origin"][0] + imin * a[0] + jmin * b[0] + kmin * c[0]
        origin[1] = self.grid["origin"][1] + imin * a[1] + jmin * b[1] + kmin * c[1]
        origin[2] = self.grid["origin"][2] + imin * a[2] + jmin * b[2] + kmin * c[2]

        # estimate memory requirement for padded data
        # in GByte by assuming double precision
        data_size = (nx * ny * nz * num_cells * 8 * 6) / 1e9
        if data_size > float(memory_limit.split()[0]):
            print(
                'Warning! Memory consumption %g GByte gets too large. Use method ="puzzle" instead!'
                % data_size
            )
            quit()

        ipad = imax - imin - 1
        jpad = jmax - jmin - 1
        kpad = kmax - kmin - 1

        data = np.float32(self.data)
        padded_data = np.pad(
            data, [(0, ipad * nx), (0, jpad * ny), (0, kpad * nz)], mode="wrap"
        )

        nx = (imax - imin) * nx
        ny = (jmax - jmin) * ny
        nz = (kmax - kmin) * nz
        a_grid = np.linspace(imin, imax, nx, endpoint=False)
        b_grid = np.linspace(jmin, jmax, ny, endpoint=False)
        c_grid = np.linspace(kmin, kmax, nz, endpoint=False)
        A, B, C = np.meshgrid(a_grid, b_grid, c_grid, indexing="ij")

        X = A * a[0] + B * b[0] + C * c[0]
        Y = A * a[1] + B * b[1] + C * c[1]
        Z = A * a[2] + B * b[2] + C * c[2]
        inside = (X >= boundary["x"][0]) * (X <= boundary["x"][1])
        inside *= (Y >= boundary["y"][0]) * (Y <= boundary["y"][1])
        inside *= (Z >= boundary["z"][0]) * (Z <= boundary["z"][1])

        expanded_surfaces = []

        for surface in self.isosurface:
            isovalue = surface["isovalue"]
            iso = isovalue * self.data.max()
            color = surface["color"]

            v_, f, normals, values = measure.marching_cubes(
                padded_data, iso, mask=inside
            )
            v = np.zeros_like(v_)

            v_[:, 0] /= nx
            v_[:, 1] /= ny
            v_[:, 2] /= nz
            v[:, 0] = (
                origin[0]
                + v_[:, 0] * a[0] * (ipad + 1)
                + v_[:, 1] * b[0] * (jpad + 1)
                + v_[:, 2] * c[0] * (kpad + 1)
            )
            v[:, 1] = (
                origin[1]
                + v_[:, 0] * a[1] * (ipad + 1)
                + v_[:, 1] * b[1] * (jpad + 1)
                + v_[:, 2] * c[1] * (kpad + 1)
            )
            v[:, 2] = (
                origin[2]
                + v_[:, 0] * a[2] * (ipad + 1)
                + v_[:, 1] * b[2] * (jpad + 1)
                + v_[:, 2] * c[2] * (kpad + 1)
            )

            expanded_surfaces.append(
                {
                    "isovalue": isovalue,
                    "color": color,
                    "vertices": v,
                    "faces": f,
                    "normals": normals,
                }
            )

        return expanded_surfaces

    def set_colordata(
        self,
        colordata,
        color_min=-np.pi,
        color_max=+np.pi,
        color_num=256,
        color_type="phase",
    ):
        # WARNING! this only work for orthogonal grid basis vectors a, b and c !!

        color_map = self._set_colormap(color_min, color_max, color_num, color_type)

        # print(color_map)

        import scipy.interpolate as interp

        a, b, c = self.grid["a"][0], self.grid["b"][1], self.grid["c"][2]
        nx, ny, nz = self.grid["nx"], self.grid["ny"], self.grid["nz"]
        origin = self.grid["origin"]
        x = np.linspace(origin[0], origin[0] + a, nx)
        y = np.linspace(origin[1], origin[1] + b, ny)
        z = np.linspace(origin[2], origin[2] + c, nz)

        if color_type == "phase":
            phase = np.exp(1j * colordata)
            color_interp = interp.RegularGridInterpolator(
                (x, y, z), phase, bounds_error=False, fill_value=np.nan
            )
        else:
            color_interp = interp.RegularGridInterpolator(
                (x, y, z), colordata, bounds_error=False, fill_value=np.nan
            )

        for count, surface in enumerate(self.isosurface):
            color_index = []
            for vertex in surface["vertices"]:
                if color_type == "phase":
                    p = color_interp(vertex)
                    c = np.angle(p)
                    i = int(color_num / 2 + (color_num / (color_max - color_min)) * c)
                else:
                    c = color_interp(vertex)
                    i = int((color_num / (color_max - color_min)) * c)

                i = max(0, i)
                i = min(color_num - 1, i)
                color_index.append(i)
            color_index = np.array(color_index)

            self.isosurface[count]["color_index"] = color_index
            self.isosurface[count]["color_map"] = color_map

        return

    def get_isocolor(self, index):
        isocolors = self.settings["isosurface"]["colors"].split(",")
        isocolor = isocolors[index].strip()
        if "texture" in isocolor:
            color = isocolor
        else:
            color = self.settings["colors"][isocolor]

        return color

    def translate(self, vector):
        # translate structure by vector which is giben in Cartesian coordinates

        # translate structure
        if self.structure != None:
            coordinates = self.structure["atomic_coordinates"]
            for i in [0, 1, 2]:
                coordinates[:, i] += vector[i]
            self.structure["atomic_coordinates"] = coordinates

        # translate data
        if len(self.data) != 0:
            for count, surface in enumerate(self.isosurface):
                v = surface["vertices"]
                for i in [0, 1, 2]:
                    v[:, i] += vector[i]
                self.isosurface[count]["vertices"] = v

    def rotate(self, phi, theta, psi):
        # rotate around origin using Euler angles phi, theta, psi

        # get rotational matrix
        r = self.compute_Euler_matrix(phi, theta, psi)

        # rotate structure
        if self.structure != None:
            coordinates = self.structure["atomic_coordinates"]
            for count, xyz in enumerate(coordinates):
                new_xyz = np.dot(r, xyz)
                coordinates[count, :] = new_xyz
            self.structure["atomic_coordinates"] = coordinates

        # rotate data
        if len(self.data) != 0:
            for count, surface in enumerate(self.isosurface):
                v = surface["vertices"]
                for i, vertex in enumerate(v):
                    new_vertex = np.dot(r, vertex)
                    v[i, :] = new_vertex
                self.isosurface[count]["vertices"] = v

    def set_camera(self, camera_settings):
        for key in camera_settings:
            self.local_settings[key] = camera_settings[key]

    def write_povfile(self, filename, append=False, add_stuff=None):
        self.pov_file = filename

        if not append:
            file = open(filename, "w")

            self._write_header(file)
            self._write_macros(file)
        else:
            file = open(filename, "a+")

        if add_stuff != None:
            print(add_stuff, file=file)

        if self.structure != None:
            self._write_atoms(file)
            self._write_bonds(file)

        if len(self.data) != 0:
            for surface in self.isosurface:
                isovalue = surface["isovalue"]
                v = surface["vertices"]
                f = surface["faces"]
                normals = surface["normals"]

                if "color_index" in surface:
                    cmap = surface["color_map"]
                    cindex = surface["color_index"]
                    self._write_colorisosurface(
                        file, isovalue, v, f, normals, cindex, cmap
                    )

                else:
                    color = surface["color"]
                    self._write_isosurface(file, isovalue, v, f, normals, color)

        file.close()

    def run_povray(self, executable="povray"):
        import os

        os.system(executable + " " + self.pov_file)

    def _set_colormap(self, value_min, value_max, num, color_type):
        if color_type == "phase":
            #            colors = [[0,   0,   1  , 0.2],
            #                      [0.2, 0.2, 0.2, 0.2],
            #                      [1,   1,   0,   0.2],
            #                      [1,   1,   1,   0.2],
            #                      [0,   0,   1,   0.2] ]
            #            colors = [[1,   0,   0  , 0.2],
            #                      [0,   0 ,  1, 0.2],
            #                      [1,   0,   0,   0.2],
            #                      [0,   0,   1,   0.2],
            #                      [1,   0,   0,   0.2] ]
            colors = [
                [1, 1, 0, 0.2],
                [1, 0, 0, 0.2],
                [0, 0, 1, 0.2],
                [0, 1, 0, 0.2],
                [1, 1, 0, 0.2],
            ]
            value_range = value_max - value_min
            intervals = [
                value_min,
                value_min + 0.25 * value_range,
                value_min + 0.50 * value_range,
                value_min + 0.75 * value_range,
                value_max,
            ]

        elif color_type == "kmap":
            colors = [[1, 1, 1, 1.0], [1, 0, 0, 0.2]]
            value_range = value_max - value_min
            intervals = [value_min, value_max]

        value_grid = np.linspace(value_min, value_max, num)
        color_map = []
        i, j = 0, 1
        for value in value_grid:
            if value > intervals[j]:
                i += 1
                j += 1
            r1, g1, b1, t1 = colors[i][0], colors[i][1], colors[i][2], colors[i][3]
            r2, g2, b2, t2 = colors[j][0], colors[j][1], colors[j][2], colors[j][3]
            x1 = intervals[i]
            x2 = intervals[j]
            r = r1 + (r2 - r1) / (x2 - x1) * (value - x1)
            g = g1 + (g2 - g1) / (x2 - x1) * (value - x1)
            b = b1 + (b2 - b1) / (x2 - x1) * (value - x1)
            t = t1 + (t2 - t1) / (x2 - x1) * (value - x1)
            color_map.append([r, g, b, t])

        return color_map

    def _write_atoms(self, file):
        coordinates = self.structure["atomic_coordinates"]
        Z_list = self.structure["chemical_numbers"]

        print("// Atoms", file=file)
        for Z, xyz in zip(Z_list, coordinates):
            element = number2symbol[Z]
            return_var = self._get_atomsetting(element)
            x, y, z = xyz[0], xyz[1], xyz[2]
            r = return_var[0]
            if len(return_var) > 2:
                R, G, B, T = return_var[1], return_var[2], return_var[3], return_var[4]
                print(
                    "a(%g,%g,%g,%g,%g,%g,%g,%g)" % (x, y, z, r, R, G, B, T), file=file
                )

            else:
                print("a2(%g,%g,%g,%g,%s)" % (x, y, z, r, return_var[1]), file=file)

        print("\n", file=file)

    def _write_bonds(self, file):
        coordinates = self.structure["atomic_coordinates"]
        Z_list = self.structure["chemical_numbers"]
        print("// Bonds", file=file)
        for bond in self.bonds:
            i, j = bond[0], bond[1]
            Z1, Z2 = Z_list[i], Z_list[j]
            element1, element2 = number2symbol[Z1], number2symbol[Z2]

            if self.settings["bonds"]["color"] == "automatic":
                x1, y1, z1 = coordinates[i][0], coordinates[i][1], coordinates[i][2]
                x2, y2, z2 = coordinates[j][0], coordinates[j][1], coordinates[j][2]
                xm, ym, zm = 0.5 * (x1 + x2), 0.5 * (y1 + y2), 0.5 * (z1 + z2)
                radius = float(self.settings["bonds"]["radius"])

                return_var = self._get_atomsetting(element1)
                r1 = return_var[0]
                if len(return_var) > 2:
                    R1, G1, B1, T1 = (
                        return_var[1],
                        return_var[2],
                        return_var[3],
                        return_var[4],
                    )
                    print(
                        "b(%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g)"
                        % (x1, y1, z1, radius, xm, ym, zm, radius, R1, G1, B1, T1),
                        file=file,
                    )
                else:
                    print(
                        "b2(%g,%g,%g,%g,%g,%g,%g,%g,%s)"
                        % (x1, y1, z1, radius, xm, ym, zm, radius, return_var[1]),
                        file=file,
                    )

                return_var = self._get_atomsetting(element2)
                r2 = return_var[0]
                if len(return_var) > 2:
                    R2, G2, B2, T2 = (
                        return_var[1],
                        return_var[2],
                        return_var[3],
                        return_var[4],
                    )
                    print(
                        "b(%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g)"
                        % (xm, ym, zm, radius, x2, y2, z2, radius, R2, G2, B2, T2),
                        file=file,
                    )
                else:
                    print(
                        "b2(%g,%g,%g,%g,%g,%g,%g,%g,%s)"
                        % (xm, ym, zm, radius, x2, y2, z2, radius, return_var[1]),
                        file=file,
                    )

        print("\n", file=file)

    def _write_isosurface(self, file, isovalue, vertices, faces, normals, color):
        print("//Isosurface for isovalue = %g" % isovalue, file=file)

        print("mesh2 { \n vertex_vectors { %i" % len(vertices), file=file)
        for v in vertices:
            print(",<%g,%g,%g>" % (v[0], v[1], v[2]), file=file)
        print("}", file=file)

        if self.settings["isosurface"]["smooth"] == "True":
            print("normal_vectors { %i" % len(normals), file=file)
            for n in normals:
                print(",<%g,%g,%g>" % (n[0], n[1], n[2]), file=file)
            print("}", file=file)

        if "texture" in color:
            print("texture_list { 1, %s }" % color, file=file)
        else:
            print(
                "texture_list { 1, texture{pigment{rgbt<%s>} translucentFinish(0)} }"
                % color,
                file=file,
            )

        print("face_indices { %i" % len(faces), file=file)
        for f in faces:
            print(",<%i,%i,%i>, 0,0,0" % (f[0], f[1], f[2]), file=file)
        print("}", file=file)
        print("}\n", file=file)

    def _write_colorisosurface(
        self, file, isovalue, vertices, faces, normals, cindex, cmap
    ):
        print("//Isosurface for isovalue = %g" % isovalue, file=file)

        print("mesh2 { \n vertex_vectors { %i" % len(vertices), file=file)
        for v in vertices:
            print(",<%g,%g,%g>" % (v[0], v[1], v[2]), file=file)
        print("}", file=file)

        if self.settings["isosurface"]["smooth"] == "True":
            print("normal_vectors { %i" % len(normals), file=file)
            for n in normals:
                print(",<%g,%g,%g>" % (n[0], n[1], n[2]), file=file)
            print("}", file=file)

        print("texture_list { %i" % (len(cmap)), file=file)
        for rgbt in cmap:
            r, g, b, t = rgbt[0], rgbt[1], rgbt[2], rgbt[3]
            print(
                "texture{pigment{rgbt<%g,%g,%g,%g>} translucentFinish(0)}"
                % (r, g, b, t),
                file=file,
            )
        print(" }", file=file)

        print("face_indices { %i" % len(faces), file=file)
        for f in faces:
            print(
                ",<%i,%i,%i>, %i,%i,%i"
                % (f[0], f[1], f[2], cindex[f[0]], cindex[f[1]], cindex[f[2]]),
                file=file,
            )
        print("}", file=file)
        print("}\n", file=file)

    def _get_atomsetting(self, element):
        if element in self.settings["atoms"].keys():
            setting = self.settings["atoms"][element]

        else:
            setting = self.settings["atoms"]["default"]

        words = setting.split(",")
        r = float(words[0])  # radius
        if len(words) > 2:  # color specified as RGBT
            R = float(words[1])  # red
            G = float(words[2])  # green
            B = float(words[3])  # blue
            T = float(words[4])  # transparency
            return r, R, G, B, T

        else:
            if not "texture" in words[1]:
                color = self.settings["colors"][words[1].strip()].split(",")
                R = float(color[0])  # red
                G = float(color[1])  # green
                B = float(color[2])  # blue
                T = float(color[3])  # transparency
                return r, R, G, B, T

            else:
                return r, words[1].strip()

    def _write_header(self, file):
        print(
            """
#version 3.7;
#declare Width = 500;
#declare Height = 500;
#declare minScreenDimension = 500;
#declare noShadows = false;
#include "colors.inc"
#include "metals.inc"
#include "textures.inc"
""",
            file=file,
        )

        # camera settings, background and light
        if self.settings["camera"]["perspective"] == "True":
            perspective = "perspective"
        else:
            perspective = ""

        if "location" in self.local_settings:
            location = self.local_settings["location"]
        else:
            location = self.settings["camera"]["location"]

        if "look_at" in self.local_settings:
            look_at = self.local_settings["look_at"]
        else:
            look_at = self.settings["camera"]["look_at"]

        print(
            "camera{ \n %s location \n %s \n look_at %s"
            % (perspective, location, look_at),
            file=file,
        )

        keywords = ["right", "up", "sky", "angle"]
        for keyword in keywords:
            if keyword in self.local_settings:
                value = self.local_settings[keyword]
                print("%s %s" % (keyword, value), file=file)
            elif keyword in self.settings["camera"].keys():
                value = self.settings["camera"][keyword]
                print("%s %s" % (keyword, value), file=file)

        print("}", file=file)

        # background
        rgb = self.settings["background"]["rgb"]
        print("background { color rgb %s }" % (rgb), file=file)

        # light_source
        position = self.settings["light_source"]["position"]
        rgb = self.settings["light_source"]["rgb"]
        print("light_source {%s rgb %s }" % (position, rgb), file=file)

    def _write_macros(self, file):
        print(
            """
#default { finish {
  ambient 0.45
  diffuse 0.84
  specular 0.22
  roughness .00001
  metallic
  phong 0.9
  phong_size 120
}}

#macro check_shadow()
 #if (noShadows)
  no_shadow 
 #end
#end

#declare slabZ = 0;
#declare depthZ = 2147483647;
#declare dzSlab = 10;
#declare dzDepth = dzSlab;
#declare dzStep = 0.001;

#macro translucentFinish(T)
 #local shineFactor = T;
 #if (T <= 0.25)
  #declare shineFactor = (1.0-4*T);
 #end
 #if (T > 0.25)
  #declare shineFactor = 0;
 #end
 finish {
  ambient 0.45
  diffuse 0.84
  specular 0.22
  roughness .00001
  metallic shineFactor
  phong 0.9*shineFactor
  phong_size 120*shineFactor
}#end

#macro a(X,Y,Z,RADIUS,R,G,B,T)
 sphere{<X,Y,Z>,RADIUS
  pigment{rgbt<R,G,B,T>}
  translucentFinish(T)
  check_shadow()}
#end

#macro a2(X,Y,Z,RADIUS,TEXT)
 sphere{<X,Y,Z>,RADIUS
  texture{TEXT}
  check_shadow()}
#end

#macro b(X1,Y1,Z1,RADIUS1,X2,Y2,Z2,RADIUS2,R,G,B,T)
 cone{<X1,Y1,Z1>,RADIUS1,<X2,Y2,Z2>,RADIUS2
  pigment{rgbt<R,G,B,T>}
  translucentFinish(T)
  check_shadow()}
#end

#macro b2(X1,Y1,Z1,RADIUS1,X2,Y2,Z2,RADIUS2,TEXT)
 cone{<X1,Y1,Z1>,RADIUS1,<X2,Y2,Z2>,RADIUS2
  texture{TEXT}
  check_shadow()}
#end
""",
            file=file,
        )

    def internal_to_cartesian(self, internal):
        a = self.structure["cell"][0, :]
        b = self.structure["cell"][1, :]
        c = self.structure["cell"][2, :]
        cartesian = np.zeros_like(internal)
        cartesian[:, 0] = (
            internal[:, 0] * a[0] + internal[:, 1] * b[0] + internal[:, 2] * c[0]
        )
        cartesian[:, 1] = (
            internal[:, 0] * a[1] + internal[:, 1] * b[1] + internal[:, 2] * c[1]
        )
        cartesian[:, 2] = (
            internal[:, 0] * a[2] + internal[:, 1] * b[2] + internal[:, 2] * c[2]
        )

        return cartesian

    def cartesian_to_internal(self, cartesian):
        b1 = self.structure["reciprocal"][0, :]
        b2 = self.structure["reciprocal"][1, :]
        b3 = self.structure["reciprocal"][2, :]
        c1 = (
            cartesian[:, 0] * b1[0] + cartesian[:, 1] * b1[1] + cartesian[:, 2] * b1[2]
        ) / (2 * np.pi)
        c2 = (
            cartesian[:, 0] * b2[0] + cartesian[:, 1] * b2[1] + cartesian[:, 2] * b2[2]
        ) / (2 * np.pi)
        c3 = (
            cartesian[:, 0] * b3[0] + cartesian[:, 1] * b3[1] + cartesian[:, 2] * b3[2]
        ) / (2 * np.pi)
        internal = np.array([c1, c2, c3]).T
        return internal

    def compute_Euler_matrix(self, phi, theta, psi):
        """Compute rotation matrix according to Eq. (M3.10.3) of Lang-Pucker.

        Args:
        phi (float): Phi (first rotation) angle in degrees.
        theta (float): Theta (second rotation) angle in degrees.
        psi (float): Psi (third rotation) angle in degrees.

        Returns:
        (array): 3x3 Rotation matrix.
        """

        # Compute sines and cosines of angles
        sin_phi = np.sin(np.radians(phi))
        cos_phi = np.cos(np.radians(phi))
        sin_theta = np.sin(np.radians(theta))
        cos_theta = np.cos(np.radians(theta))
        sin_psi = np.sin(np.radians(psi))
        cos_psi = np.cos(np.radians(psi))

        # Euler matrix r according to eq. (M3.10.3) of Lang-Pucker
        r = np.zeros((3, 3))
        r[0, 0] = cos_phi * cos_psi - sin_phi * cos_theta * sin_psi
        r[1, 0] = -cos_phi * sin_psi - sin_phi * cos_theta * cos_psi
        r[2, 0] = sin_phi * sin_theta

        r[0, 1] = sin_phi * cos_psi + cos_phi * cos_theta * sin_psi
        r[1, 1] = -sin_phi * sin_psi + cos_phi * cos_theta * cos_psi
        r[2, 1] = -cos_phi * sin_theta

        r[0, 2] = sin_theta * sin_psi
        r[1, 2] = sin_theta * cos_psi
        r[2, 2] = cos_theta

        return r
