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

cubefile    = open(data_path + 'pentacene_HOMO.cube').read()  # read cube-file from file
homo        = Orbital(cubefile)    # compute 3D Fourier transform (see Eqs. 6-11) 
 
real_space  = False   # True: real space plot, False: momentum space plots
if real_space:
    orbital_slices = SlicedData.init_from_orbital_psi(homo)  
else:
    orbital_slices = SlicedData.init_from_orbital_psik(homo) 

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

