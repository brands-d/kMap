# This script computes the datacube Intensity[BE,kx,ky] as SlicedData object 
# (BE = binding energy)
# To this end a list of molecular orbitals is loaded from a list of URLs 
# pointing to the cube files. By using the orbital energies and a given
# energy broadening parameter the data cube is created and can be sliced as desired.
# Here, orbitals of a particular symmetry can be selected, e.g. (pi or sigma)

# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.database import Database
from kmap.library.sliceddata import SlicedData

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../../kmap/resources/misc')

db = Database(data_path / 'molecules.txt')
molecule = db.get_molecule_by_ID(406)  # choose ID from database (406 = bisanthene, PBE-functional)

# set name and select list of orbitals 
name         = 'bisanthene'   # set name for SlicedData Object
hdf5_name    = 'bisanthene_ID406.hdf5' # choose name fpr hdf5-file to be written 
energy_range = [-13, -2]       # select a binding energy range
pi           = ['au','b2g','b3g','b1u']
sigma        = ['ag','b1g','b2u','b3u']
selected_symmetry = pi + sigma   # choose between pi or sigma orbitals


orbitals     = []
for orbital in molecule.orbitals:
    if  (energy_range[0] <= orbital.energy <= energy_range[1]) and \
        orbital.symmetry in selected_symmetry:
        orbitals.append([orbital.URL,{'energy':orbital.energy,'name':orbital.name}])


# set parameters
parameters =[40.0,  # photon_energy (float): Photon energy in eV.
             0.0,   # fermi_energy (float): Fermi energy in eV
             0.2,   # energy_broadening (float): FWHM of Gaussian energy broadenening in eV
             0.03,  # dk (float): Desired k-resolution in kmap in Angstroem^-1. 
             0,     # phi (float): Euler orientation angle phi in degree. 
             0,     # theta (float): Euler orientation angle phi in degree. 
             0,     # psi (float): Euler orientation angle phi in degree. 
             'no',  # Ak_type (string): Treatment of |A.k|^2: either 'no', 'toroid' or 'NanoESCA'.  
             'p',   # polarization (string): Either 'p', 's', 'C+', 'C-' or 'CDAD'. 
             0,     # alpha (float): Angle of incidence plane in degree. 
             0,     # beta (float): Azimuth of incidence plane in degree.
             'auto',# gamma (float/str): Damping factor for final state in Angstroem^-1. str = 'auto' sets gamma automatically
             'no']  # symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                    #    '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
             
# initialize SlicedData object
kmap_stack = SlicedData.init_from_orbitals(name,orbitals,parameters)  
kmap_stack.write_hdf5(hdf5_name)

