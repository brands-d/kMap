# ATTENTION SCRIPT NOT WORKING

# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.database import Database
from kmap.library.sliceddata import SlicedData

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

db = Database(str(data_path / 'molecules.txt'))
molecule = db.get_molecule_by_ID(11)  # choose pentacene molecule for testing ...

# set name and select list of orbitals 
name     = 'pentacene-HOMO-hnu'   # set name for SlicedData Object
i        = -4                     # choose one orbital. Here: HOMO of pentacene
orbital  = [[molecule.orbitals[i].URL,
           {'energy':molecule.orbitals[i].energy,'name':molecule.orbitals[i].name}]]

# set parameters
parameters =[20,    # minimal photon_energy (float)
             100,   # maximal photon_energy (float)
             2,     # step size for photon_energy (float)
             0.0,   # fermi_energy (float): Fermi energy in eV
             0.02,  # dk (float): Desired k-resolution in kmap in Angstroem^-1. 
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
kmap_stack = SlicedData.init_from_orbital_photonenergy(name,orbital,parameters)  

# Plot some slices
fig, _ax = plt.subplots(3,3)
ax = _ax.flatten()
nplots = len(ax)
nslice = kmap_stack.data.shape[0]

count = 0
for i in range(0,nslice,1+nslice//nplots):
    plot_data = kmap_stack.slice_from_index(i)
    ax[count].imshow(plot_data.data)
    count += 1
plt.show()

