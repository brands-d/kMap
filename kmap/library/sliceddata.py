import logging
import os
import urllib.request
from pathlib import Path

import h5py
import numpy as np

from kmap.config.config import config
from kmap.library.abstractdata import AbstractData
from kmap.library.axis import Axis
from kmap.library.id import ID as IDD
from kmap.library.misc import energy_to_k, get_remote_hdf5_orbital, write_cube
from kmap.library.orbital import Orbital
from kmap.library.plotdata import PlotData


class SlicedData(AbstractData):
    def __init__(self, name, axis_1, axis_2, axis_3, data, meta_data={}, ID=None):
        if isinstance(name, str) and name:
            if ID is not None:
                super(SlicedData, self).__init__(ID, name, meta_data)
            else:
                super(SlicedData, self).__init__(IDD.new_ID(), name, meta_data)

        else:
            raise ValueError("name has to be string and not empty")

        data = np.array(data, dtype=np.float64)
        if len(data.shape) == 3:
            self.data = data

        else:
            raise ValueError("data has to be 3D")

        axis_1 = Axis.init_from_hdf_list(axis_1, len(data[:, 0, 0]))
        axis_2 = Axis.init_from_hdf_list(axis_2, len(data[0, :, 0]))
        axis_3 = Axis.init_from_hdf_list(axis_3, len(data[0, 0, :]))
        self.axes = [axis_1, axis_2, axis_3]

    @classmethod
    def init_from_hdf5(cls, file_path, keys={}, meta_data={}, ID=None):
        # Updates default file_keys with user defined keys
        file_keys = {
            "name": "name",
            "axis_1_label": "axis_1_label",
            "axis_1_units": "axis_1_units",
            "axis_1_range": "axis_1_range",
            "axis_2_label": "axis_2_label",
            "axis_2_units": "axis_2_units",
            "axis_2_range": "axis_2_range",
            "axis_3_label": "axis_3_label",
            "axis_3_units": "axis_3_units",
            "axis_3_range": "axis_3_range",
            "data": "data",
        }
        file_keys.update(keys)

        with h5py.File(file_path, "r") as file:
            # First check if necessary datasets exist
            for _, value in file_keys.items():
                if value not in file:
                    raise AttributeError("Dataset is missing %s" % value)

            # Read all datasets
            for key, value in file.items():
                if key == file_keys["name"]:
                    name = str(file[key].asstr()[...])

                elif key == file_keys["axis_1_label"]:
                    axis_1_label = str(file[key].asstr()[...])

                elif key == file_keys["axis_2_label"]:
                    axis_2_label = str(file[key].asstr()[...])

                elif key == file_keys["axis_3_label"]:
                    axis_3_label = str(file[key].asstr()[...])
                elif key == file_keys["axis_1_units"]:
                    axis_1_units = str(file[key].asstr()[...])

                elif key == file_keys["axis_2_units"]:
                    axis_2_units = str(file[key].asstr()[...])

                elif key == file_keys["axis_3_units"]:
                    axis_3_units = str(file[key].asstr()[...])

                elif key == file_keys["axis_1_range"]:
                    axis_1_range = file[key][()]

                elif key == file_keys["axis_2_range"]:
                    axis_2_range = file[key][()]

                elif key == file_keys["axis_3_range"]:
                    axis_3_range = file[key][()]

                elif key == file_keys["data"]:
                    data = file[key][()]

                else:
                    try:
                        meta_data.update({key: str(file[key].asstr()[...])})

                    except:
                        meta_data.update({key: str(file[key][()])})

        axis_1 = [axis_1_label, axis_1_units, axis_1_range]
        axis_2 = [axis_2_label, axis_2_units, axis_2_range]
        axis_3 = [axis_3_label, axis_3_units, axis_3_range]

        self = cls(name, axis_1, axis_2, axis_3, data, meta_data)
        if ID is not None:
            self.ID = ID

        return self

    @classmethod
    def init_from_orbitals(cls, name, orbitals, parameters, s_share=0.694, ID=None):
        """Returns a SlicedData object with the data[BE,kx,ky]
           computed from the kmaps of several orbitals and
           broadened in energy.

        Args:
            name (str): name for SlicedData object
            orbitals (list): [[ 'URL1',dict1], ['URL2',dict2], ...]
                dict needs keys: 'energy' and 'name'
            parameters (list): list of parameters
                photon_energy (float): Photon energy in eV.
                fermi_energy (float): Fermi energy in eV
                energy_broadening (float): FWHM of Gaussian energy broadenening in eV
                dk (float): Desired k-resolution in kmap in Angstroem^-1.
                phi (float): Euler orientation angle phi in degree.
                theta (float): Euler orientation angle theta in degree.
                psi (float): Euler orientation angle psi in degree.
                Ak_type (string): Treatment of |A.k|^2: either 'no',
                        'toroid' or 'NanoESCA'.
                polarization (string): Either 'p', 's', 'unpolarized', C+', 'C-' or
                        'CDAD'.
                alpha (float): Angle of incidence plane in degree.
                beta (float): Azimuth of incidence plane in degree.
                gamma (float/str): Damping factor for final state in
                        Angstroem^-1. str = 'auto' sets gamma automatically
                symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                        '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
            s_share (float): Share of s polarized light in unpolarized light.
        Returns:
            (SlicedData): SlicedData containing kmaps of all orbitals
        """

        log = logging.getLogger("kmap")
        # extract parameters
        photon_energy = parameters[0]
        fermi_energy = parameters[1]
        energy_broadening = parameters[2]
        dk = parameters[3]
        phi, theta, psi = parameters[4], parameters[5], parameters[6]
        Ak_type = parameters[7]
        polarization = parameters[8]
        alpha, beta, gamma = parameters[9], parameters[10], parameters[11]
        symmetrization = parameters[12]

        # determine axis_1 from minimal and maximal binding energy
        extend_range = 3 * energy_broadening
        energies = []

        for orbital in orbitals:
            energies.append(orbital[1]["energy"])

        BE_min = min(energies) - fermi_energy - extend_range
        BE_max = max(energies) - fermi_energy + extend_range
        # set energy grid spacing 6 times smaller than broadening
        dBE = energy_broadening / 6
        nBE = int((BE_max - BE_min) / dBE) + 1
        BE = np.linspace(BE_min, BE_max, nBE)
        nBE = len(BE)
        axis_1 = ["-BE", "eV", [BE_min, BE_max]]

        # determine axis_2 and axis_3 kmax at BE_max
        Phi = -fermi_energy  # work function
        E_kin_max = photon_energy - Phi + BE_max
        k_max = energy_to_k(E_kin_max)
        nk = int((2 * k_max) / dk) + 1
        k_grid = np.linspace(-k_max, +k_max, nk)
        nk = len(k_grid)
        axis_2 = ["kx", "1/Å", [-k_max, +k_max]]
        axis_3 = ["ky", "1/Å", [-k_max, +k_max]]

        # initialize 3D-numpy array with zeros
        data = np.zeros((nBE, nk, nk))
        orbital_names = []

        # add kmaps of orbitals to
        log.info("Adding orbitals to SlicedData Object, please wait!")
        for orbital in orbitals:
            # binding energy of orbital
            BE0 = orbital[1]["energy"] - fermi_energy
            # kinetic energy of emitted electron
            E_kin = photon_energy - Phi + BE0

            # Gaussian weight function
            norm = 1 / np.sqrt(2 * np.pi * energy_broadening**2)
            weight = norm * np.exp(-((BE - BE0) ** 2 / (2 * energy_broadening**2)))

            url = orbital[0]

            file, file_format = SlicedData.load_orbital_online(orbital)
            orbital_data = Orbital(file, file_format)
            orbital_names.append(orbital[1]["name"])
            log.info("Computing k-map for %s" % orbital[1]["name"])

            kmap = orbital_data.get_kmap(
                E_kin,
                dk,
                phi,
                theta,
                psi,
                Ak_type,
                polarization,
                alpha,
                beta,
                gamma,
                symmetrization,
                s_share=s_share,
            )
            kmap.interpolate(k_grid, k_grid, update=True)
            log.info("Adding to 3D-array: %s" % orbital[1]["name"])
            for i in range(len(BE)):
                data[i, :, :] += weight[i] * np.nan_to_num(kmap.data)

        # set NaNs outside photoemission horizon
        KX, KY = np.meshgrid(k_grid, k_grid)
        for i in range(len(BE)):
            E_kin = photon_energy - Phi + BE[i]
            k_max = energy_to_k(E_kin)
            out = np.sqrt(KX**2 + KY**2) > k_max
            tmp = data[i, :, :]
            tmp[out] = np.NaN
            data[i, :, :] = tmp

        # define meta-data for tool-tip display
        orbital_info = {}
        for orbital_name, energy in zip(orbital_names, energies):
            orbital_info[orbital_name] = energy

        meta_data = {
            "Photon energy (eV)": photon_energy,
            "Fermi energy (eV)": fermi_energy,
            "Energy broadening (eV)": energy_broadening,
            "Molecular orientation": (phi, theta, psi),
            "|A.k|^2 factor": Ak_type,
            "Polarization": polarization,
            "Incidence direction": (alpha, beta),
            "Symmetrization": symmetrization,
            "Orbital Info": orbital_info,
        }

        return cls(name, axis_1, axis_2, axis_3, data, meta_data, ID=ID)

    @classmethod
    def init_from_orbital_cube(cls, name, orbital, parameters, ID=None):
        """Returns a SlicedData object with the data[x,y,z]
           taken from the real space wave function in orbital.

        Args:
            name (str): name for SlicedData object
            orbital (list): [ 'URL',dict ]
                dict needs keys: 'energy' and 'name'
            parameters (list): list of parameters
                domain (str): either 'real-space' or 'k-space'
                dk3D (float): Desired resolution for 3D-Fourier-Transform.
                    Single number.
                E_kin_max (float): maximum kinetic energy in eV is used to
                    reduce the size of the 3D-numpy-array in momentum space
                value (string): choose between 'real', 'imag', 'abs' or 'abs2'
                    for Re(), Im(), |..| or |..|^2

        Returns:
            (SlicedData): SlicedData containing the real space orbital
        """
        log = logging.getLogger("kmap")

        orbital = orbital[0]  # only consider first orbital in list!

        # extract parameters
        domain = parameters[0]
        dk3D = parameters[1]
        E_kin_max = parameters[2]
        value = parameters[3]

        orbital_file = orbital[0]

        # decision if reading cube-file from URL or local file
        if orbital_file[:4] == "http":
            file, file_format = SlicedData.load_orbital_online(orbital)
            orbital_data = Orbital(
                file,
                dk3D=dk3D,
                E_kin_max=E_kin_max,
                value=value,
                file_format=file_format,
                orbital_name=orbital[1]["name"],
            )
        else:
            file = open(orbital_file).read()
            orbital_data = Orbital(file, dk3D=dk3D, E_kin_max=E_kin_max, value=value)

        # set name for SliceData object
        name = orbital_data.psi["name"]

        # set axis and data
        if domain == "real-space":
            axis_1 = ["x", "Å", [orbital_data.psi["x"][0], orbital_data.psi["x"][-1]]]
            axis_2 = ["y", "Å", [orbital_data.psi["y"][0], orbital_data.psi["y"][-1]]]
            axis_3 = ["z", "Å", [orbital_data.psi["z"][0], orbital_data.psi["z"][-1]]]
            data = orbital_data.psi["data"]

        else:
            axis_1 = [
                "kx",
                "1/Å",
                [orbital_data.psik["kx"][0], orbital_data.psik["kx"][-1]],
            ]
            axis_2 = [
                "ky",
                "1/Å",
                [orbital_data.psik["ky"][0], orbital_data.psik["ky"][-1]],
            ]
            axis_3 = [
                "kz",
                "1/Å",
                [orbital_data.psik["kz"][0], orbital_data.psik["kz"][-1]],
            ]
            data = orbital_data.psik["data"]

        # no meta data
        meta_data = {}
        return cls(name, axis_1, axis_2, axis_3, data, meta_data, ID=ID)

    @classmethod
    def init_from_orbital_photonenergy(
        cls, name, orbital, parameters, s_share=0.694, ID=None
    ):
        """Returns a SlicedData object with the data[photonenergy,kx,ky]
           computed from the kmaps of one orbital for a series of
           photon energies.

        Args:
            name (str): name for SlicedData object
            orbital (list): [ 'URL',dict ]
                dict needs keys: 'energy' and 'name'
            parameters (list): list of parameters
                hnu_min (float): minimal photon energy
                hnu_max (float): maximal photon energy
                hnu_step (float): stepsize for photon energy
                fermi_energy (float): Fermi energy in eV
                dk (float): Desired k-resolution in kmap in Angstroem^-1.
                phi (float): Euler orientation angle phi in degree.
                theta (float): Euler orientation angle theta in degree.
                psi (float): Euler orientation angle psi in degree.
                Ak_type (string): Treatment of |A.k|^2: either 'no',
                        'toroid' or 'NanoESCA'.
                polarization (string): Either 'p', 's', 'unpolarized', C+', 'C-' or
                        'CDAD'.
                alpha (float): Angle of incidence plane in degree.
                beta (float): Azimuth of incidence plane in degree.
                gamma (float/str): Damping factor for final state in
                        Angstroem^-1. str = 'auto' sets gamma automatically
                symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                        '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
                s_share (float): Share of s polarized light in unpolarized light.
        Returns:
            (SlicedData): SlicedData containing kmaps for various photon energies
        """

        log = logging.getLogger("kmap")
        orbital = orbital[0]  # only consider first orbital in list!

        # extract parameters
        hnu_min = parameters[0]
        hnu_max = parameters[1]
        hnu_step = parameters[2]
        fermi_energy = parameters[3]
        dk = parameters[4]
        phi, theta, psi = parameters[5], parameters[6], parameters[7]
        Ak_type = parameters[8]
        polarization = parameters[9]
        alpha, beta, gamma = parameters[10], parameters[11], parameters[12]
        symmetrization = parameters[13]

        # binding energy of orbital and work function
        BE = orbital[1]["energy"] - fermi_energy
        Phi = -fermi_energy  # work function

        # determine axis_1 = photon energy
        hnu = np.arange(hnu_min, hnu_max, hnu_step)
        n_hnu = len(hnu)

        axis_1 = ["photonenergy", "eV", [hnu_min, hnu_max]]

        # determine axis_2 and axis_3 kmax at BE_max
        E_kin_max = hnu[-1] - Phi + BE
        k_max = energy_to_k(E_kin_max)
        nk = int((2 * k_max) / dk) + 1
        k_grid = np.linspace(-k_max, +k_max, nk)
        nk = len(k_grid)
        axis_2 = ["kx", "1/Å", [-k_max, +k_max]]
        axis_3 = ["ky", "1/Å", [-k_max, +k_max]]

        # initialize 3D-numpy array with zeros
        data = np.zeros((n_hnu, nk, nk))
        orbital_names = []

        log.info("Adding orbital to SlicedData Object, please wait!")
        # read orbital from cube-file database
        url = orbital[0]
        file, file_format = SlicedData.load_orbital_online(orbital)
        orbital_data = Orbital(
            file, file_format=file_format, orbital_name=orbital[1]["name"]
        )

        # file = SlicedData.load_orbital_online(url)
        # orbital_data = Orbital(file)

        # loop over photon energies
        for i in range(len(hnu)):
            # kinetic energy of emitted electron
            E_kin = hnu[i] - Phi + BE
            kmap = orbital_data.get_kmap(
                E_kin,
                dk,
                phi,
                theta,
                psi,
                Ak_type,
                polarization,
                alpha,
                beta,
                gamma,
                symmetrization,
                s_share=s_share,
            )
            kmap.interpolate(k_grid, k_grid, update=True)
            data[i, :, :] = kmap.data

        # define meta-data for tool-tip display
        orbital_info = orbital[1]

        meta_data = {
            "Fermi energy (eV)": fermi_energy,
            "Molecular orientation": (phi, theta, psi),
            "|A.k|^2 factor": Ak_type,
            "Polarization": polarization,
            "Incidence direction": (alpha, beta),
            "Symmetrization": symmetrization,
            "Orbital Info": orbital_info,
        }

        return cls(name, axis_1, axis_2, axis_3, data, meta_data, ID=ID)

    @classmethod
    def load_orbital_online(cls, orbital):
        log = logging.getLogger("kmap")
        url = orbital[0]
        cache_dir = Path(config.get_key("paths", "cache"))
        cache_file = url.split("cubefiles/")[1].replace("/", "_")
        cache_file = str(cache_dir / cache_file)

        if os.path.isfile(cache_file):
            log.info(f"Found file {url} in cache.")
            with open(cache_file, "r") as f:
                file = f.read()
            file_format = "cube"

        else:
            try:
                log.info(f'Loading from ID{orbital[1]["ID"]:05d} hdf5 file....')
                molecule, psi = get_remote_hdf5_orbital(
                    "143.50.187.12",
                    "80",
                    int(float(orbital[1]["database ID"])),
                    int(orbital[1]["ID"]) - 1,
                )
                file = h5py.File("aux.hdf5", "w", driver="core", backing_store=False)
                file.create_dataset("num_atom", data=molecule["num_atom"])
                file.create_dataset(
                    "chemical_numbers", data=molecule["chemical_numbers"]
                )
                file.create_dataset(
                    "atomic_coordinates",
                    data=molecule["atomic_coordinates"],
                    dtype="float64",
                )
                file.create_dataset("x", data=psi["x"], dtype="float64")
                file.create_dataset("y", data=psi["y"], dtype="float64")
                file.create_dataset("z", data=psi["z"], dtype="float64")
                file.create_dataset("data", data=psi["data"], dtype="float64")
                name = psi["name"]
                file_format = "hdf5"

                if os.path.isdir(cache_dir):
                    log.info(f"Putting {url} into cache {cache_file}")
                    write_cube(psi, molecule, cache_file)

            except Exception as e:
                log.info("Loading from database: %s" % url)
                with urllib.request.urlopen(url) as f:
                    file = f.read().decode("utf-8")

                    if os.path.isdir(cache_dir):
                        log.info(f"Putting {url} into cache {cache_file}")
                        with open(cache_file, "w") as f:
                            f.write(file)
                file_format = "cube"

        return file, file_format

    def transpose(self, axes_order):
        self.data = self.data.transpose(axes_order)
        self.axes = [self.axes[i] for i in axes_order]

    def slice_from_index(self, index, axis=0):
        if axis == 0:
            data = self.data[index, :, :]
            range_ = [self.axes[2].range, self.axes[1].range]

        elif axis == 1:
            data = self.data[:, index, :]
            range_ = [self.axes[2].range, self.axes[0].range]

        elif axis == 2:
            data = self.data[:, :, index]
            range_ = [self.axes[1].range, self.axes[0].range]

        else:
            raise ValueError("axis has to be between 1 and 3")

        return PlotData(data, range_)

    def write_hdf5(self, hdf5_name):
        h5file = h5py.File(hdf5_name, "w")  # create new file

        h5file.create_dataset("name", data=self.name)
        h5file.create_dataset("alias", data=self.name)

        h5file.create_dataset("axis_1_label", data=self.axes[0].label)
        h5file.create_dataset("axis_2_label", data=self.axes[1].label)
        h5file.create_dataset("axis_3_label", data=self.axes[2].label)

        h5file.create_dataset("axis_1_units", data=self.axes[0].units)
        h5file.create_dataset("axis_2_units", data=self.axes[1].units)
        h5file.create_dataset("axis_3_units", data=self.axes[2].units)

        h5file.create_dataset("axis_1_range", data=self.axes[0].range)
        h5file.create_dataset("axis_2_range", data=self.axes[1].range)
        h5file.create_dataset("axis_3_range", data=self.axes[2].range)

        h5file.create_dataset("data", data=self.data, dtype="f8")

        for key in self.meta_data:
            if key != "Orbital Info":
                h5file.create_dataset(key, data=self.meta_data[key])

            else:
                for orbital in self.meta_data[key]:
                    h5file.create_dataset(orbital, data=self.meta_data[key][orbital])

        h5file.close()

    def __str__(self):
        rep = AbstractData.__str__(self)

        for index, axis in enumerate(self.axes):
            rep += "\n\nAxis %i\n%s" % (index, str(self.axes[index]))

        rep += "\n\n"
        return rep[:-2]
