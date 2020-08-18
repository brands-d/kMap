# This script demonstrates how the real space or the momentum space wave function can be
# converted into a SlicedData Object

# Python imports
import os, sys
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path + os.sep + '..' + os.sep + '..' + os.sep)
data_path = path + os.sep + '..' + os.sep + 'data' + os.sep

# kmap imports
from kmap.library.orbital import Orbital
from kmap.library.sliceddata import SlicedData

# choose local path to cube-file
cube_file   = data_path + 'pentacene_HOMO.cube'   

# ... or choose URL pointing to cubefile
# cube_file = 'http://143.50.77.12/OrganicMolecule/B3LYP/5A/charge0mult1/5A_MO_73'


# uncomment to create real-space SlicedData
#orbital_slices = SlicedData.init_from_orbital_psi(cube_file, 
#                                                  domain='real-space')  

# ... or uncomment for k-space SlicedData
orbital_slices = SlicedData.init_from_orbital_psi(cube_file, 
                                                  domain='k-space',
                                                  dk3D=0.15, 
                                                  E_kin_max=150, 
                                                  value='imag')  

# Plot some slices
fig, _ax = plt.subplots(3,3)
ax = _ax.flatten()
nplots = len(ax)
nslice = orbital_slices.data.shape[0]

count = 0
for i in range(0,nslice,1+nslice//nplots):
    plot_data = orbital_slices.slice_from_index(i)
    ax[count].imshow(plot_data.data)
    count += 1

plt.show()

