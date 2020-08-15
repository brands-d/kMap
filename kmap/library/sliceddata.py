# Python Imports
import h5py
import numpy as np
import urllib.request

# Own Imports
from kmap.library.id import ID
from kmap.library.plotdata import PlotData
from kmap.library.abstractdata import AbstractData
from kmap.library.misc import axis_from_range
from kmap.library.database import Database
from kmap.library.orbital import Orbital 


class SlicedData(AbstractData):

    def __init__(self, name, axis_1, axis_2, axis_3, data, meta_data={}):

        if isinstance(name, str) and name:
            super(SlicedData, self).__init__(ID.new_ID(), name, meta_data)

        else:
            raise ValueError('name has to be string and not empty')

        data = np.array(data, dtype=np.float64)
        if len(data.shape) == 3:
            self.data = data

        else:
            raise ValueError('data has to be 3D')

        axis_1 = Axis.init_from_hdf_list(axis_1, len(data[:, 0, 0]))
        axis_2 = Axis.init_from_hdf_list(axis_2, len(data[0, :, 0]))
        axis_3 = Axis.init_from_hdf_list(axis_3, len(data[0, 0, :]))
        self.axes = [axis_1, axis_2, axis_3]

    @classmethod
    def init_from_hdf5(cls, file_path, keys={}, meta_data={}):

        # Updates default file_keys with user defined keys
        file_keys = {'name': 'name', 'axis_1_label': 'axis_1_label',
                     'axis_1_units': 'axis_1_units',
                     'axis_1_range': 'axis_1_range',
                     'axis_2_label': 'axis_2_label',
                     'axis_2_units': 'axis_2_units',
                     'axis_2_range': 'axis_2_range',
                     'axis_3_label': 'axis_3_label',
                     'axis_3_units': 'axis_3_units',
                     'axis_3_range': 'axis_3_range',
                     'data': 'data'}
        file_keys.update(keys)

        with h5py.File(file_path, 'r') as file:

            # First check if necessary datasets exist
            for _, value in file_keys.items():
                if value not in file:
                    raise AttributeError('Dataset is missing %s' % value)

            # Read all datasets
            for key, value in file.items():
                if key == file_keys['name']:
                    name = str(file[key][()])

                elif key == file_keys['axis_1_label']:
                    axis_1_label = file[key][()]

                elif key == file_keys['axis_2_label']:
                    axis_2_label = file[key][()]

                elif key == file_keys['axis_3_label']:
                    axis_3_label = file[key][()]

                elif key == file_keys['axis_1_units']:
                    axis_1_units = file[key][()]

                elif key == file_keys['axis_2_units']:
                    axis_2_units = file[key][()]

                elif key == file_keys['axis_3_units']:
                    axis_3_units = file[key][()]

                elif key == file_keys['axis_1_range']:
                    axis_1_range = file[key][()]

                elif key == file_keys['axis_2_range']:
                    axis_2_range = file[key][()]

                elif key == file_keys['axis_3_range']:
                    axis_3_range = file[key][()]

                elif key == file_keys['data']:
                    data = file[key][()]

                else:
                    meta_data.update({key: str(file[key][()])})

        axis_1 = [axis_1_label, axis_1_units, axis_1_range]
        axis_2 = [axis_2_label, axis_2_units, axis_2_range]
        axis_3 = [axis_3_label, axis_3_units, axis_3_range]

        return cls(name, axis_1, axis_2, axis_3, data, meta_data)

    @classmethod
    def init_from_orbitals(cls, name, orbitals,  
                                photon_energy=35,  
                                fermi_energy=0,     
                                energy_broadening=0.4,  
                                dk=0.03,               
                                phi=0,theta=0,psi=0,   
                                Ak_type='no',           
                                polarization='p',
                                alpha=60,beta=90,gamma='auto',
                                symmetrization='no'):

        """Returns a SlicedData object with the data[BE,kx,ky] 
           computed from the kmaps of several orbitals and
           broadened in energy.

        Args:
            name (str): name for SlicedData object
            orbitals (list): list of orbitals from kmap.database.Orbital class
            photon_energy (float): Photon energy in eV.
            fermi_energy (float): Fermi energy in eV
            energy_broadening (float): FWHM of Gaussian energy broadenening in eV
            dk (float): Desired k-resolution in kmap in Angstroem^-1.
            phi (float): Euler orientation angle phi in degree.
            theta (float): Euler orientation angle theta in degree.
            psi (float): Euler orientation angle psi in degree.
            Ak_type (string): Treatment of |A.k|^2: either 'no',
                'toroid' or 'NanoESCA'.
            polarization (string): Either 'p', 's', 'C+', 'C-' or
                'CDAD'.   
            alpha (float): Angle of incidence plane in degree.
            beta (float): Azimuth of incidence plane in degree.
            gamma (float/str): Damping factor for final state in
                Angstroem^-1. str = 'auto' sets gamma automatically
            symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
        Returns:
            (SlicedData): SlicedData containing kmaps of all orbitals
        """

        # determine axis_1 from minimal and maximal binding energy
        extend_range = 3*energy_broadening
        energies = []
        
        for orbital in orbitals:                
            energies.append(orbital.energy)

        BE_min = min(energies) - fermi_energy - extend_range
        BE_max = max(energies) - fermi_energy + extend_range
        dBE    = energy_broadening/4  # set energy grid spacing 5 times smaller than broadening
        nBE    = int( (BE_max - BE_min)/dBE ) + 1
        BE     = np.linspace(BE_min,BE_max,nBE)
        nBE    = len(BE)
        axis_1 = ['-BE', 'eV',  [BE_min, BE_max]]

        # determine axis_2 and axis_3 kmax at BE_max
        Phi        = -fermi_energy  # work function
        E_kin_max  = photon_energy - Phi + BE_max
        m, hbar, e = 9.10938356e-31, 1.0545718e-34, 1.60217662e-19 
        fac        = 2 * 1e-20 * e * m / hbar**2
        k_max      = np.sqrt(fac * E_kin_max)
        nk         = int( (2*k_max)/dk ) + 1
        k_grid     = np.linspace(-k_max,+k_max,nk)
        nk         = len(k_grid)
        axis_2     = ['kx', '1/A', [-k_max,+k_max]]
        axis_3     = ['ky', '1/A', [-k_max,+k_max]]
  
        # initialize 3D-numpy array with zeros     
        data          = np.zeros((nBE,nk,nk))
        orbital_names = []

        # add kmaps of orbitals to 
        print('Adding orbitals to SlicedData Object, please wait!')
        for orbital in orbitals:
            BE0    = orbital.energy - fermi_energy  # binding energy of orbital
            E_kin  = photon_energy - Phi + BE0      # kinetic energy of emitted electron

            # Gaussian weight function
            norm   = (1/np.sqrt(2*np.pi*energy_broadening**2)) 
            weight = norm*np.exp( -((BE - BE0)**2/(2*energy_broadening**2)) )

            url    = orbital.URL  

            print('Loading from database: ',url)
            with urllib.request.urlopen(url) as f:
                file = f.read().decode('utf-8')
                orbital_data = Orbital(file)

            orbital_name = orbital.name
            orbital_names.append(orbital.name)
            print('Computing k-map for ',orbital_name)

            kmap = orbital_data.get_kmap(E_kin, dk, phi, theta, psi,
                                  Ak_type, polarization, alpha, beta,
                                  gamma,symmetrization)
            kmap.interpolate(k_grid,k_grid,update=True)
     
            print('Adding to 3D-array: ',orbital_name)       
            for i in range(len(BE)):
                data[i,:,:] = weight[i]*kmap.data

        # define meta-data for tool-tip display
        orbital_info = {}
        for name, energy in zip(orbital_names, energies):
            orbital_info[name] = energy    

        meta_data = {'Photon energy (eV)':photon_energy,
                     'Fermi energy (eV)':fermi_energy,
                     'Energy broadening (eV)':energy_broadening,
                     'Molecular orientation':(phi, theta, psi),
                     '|A.k|^2 factor':Ak_type,
                     'Polarization':polarization,
                     'Incidence direction':(alpha, beta),
                     'Symmetrization':symmetrization,
                     'Orbital Info':orbital_info}

        return cls(name, axis_1, axis_2, axis_3, data, meta_data)


    def slice_from_index(self, index, axis=0):

        if axis == 0:
            data = self.data[index, :, :]
            range_ = [self.axes[1].range, self.axes[2].range]

        elif axis == 1:
            data = self.data[:, index, :]
            range_ = [self.axes[0].range, self.axes[2].range]

        elif axis == 2:
            data = self.data[:, :, index]
            range_ = [self.axes[0].range, self.axes[1].range]

        else:
            raise ValueError('axis has to be between 1 and 3')

        return PlotData(data, range_)

    def __str__(self):

        rep = AbstractData.__str__(self)

        for index, axis in enumerate(self.axes):
            rep += '\n\nAxis %i\n%s' % (index, str(self.axes[index]))

        rep += '\n\n'
        return rep[:-2]


class Axis():

    def __init__(self, label, units, range_, num):

        self.label = label
        self.units = units
        self.range = range_
        self.axis = axis_from_range(range_, num)

    @classmethod
    def init_from_hdf_list(cls, axis, num):

        if Axis._is_correct_axis(axis):
            return cls(*axis, num)

    @classmethod
    def _is_correct_axis(self, axis):

        if not isinstance(axis, list) or len(axis) != 3:
            raise ValueError('axis has to be a list of length 3')

        label, units, range_ = axis
        if not isinstance(label, str) or not label:
            raise ValueError('axis label has to be a non empty string')

        if not isinstance(units, str) or not units:
            raise ValueError('axis units has to be a non empty string')

        if len(range_) != 2:
            raise ValueError('axis range has to be list of length 2')

        minimum, maximum = range_
        if not np.isfinite(minimum) or not np.isfinite(maximum):
            raise ValueError('axis range can not contain inf or nan values')

        if not minimum < maximum:
            raise ValueError(
                'axis minimum has to strictly smaller than maxmimum')

        return True

    def __str__(self):

        rep = 'Label:\t%s\nUnits:\t%s\nRange:\t[%.3f, %.3f]' % (
            self.label, self.units, *self.range)
        return rep
