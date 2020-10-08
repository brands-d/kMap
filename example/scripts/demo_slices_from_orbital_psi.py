# This script demonstrates how the real space or the momentum space wave
# function can be
# converted into a SlicedData Object

# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.sliceddata import SlicedData

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path('../data/')

# choose local path to cube-file (string because init at line 31 expects
# a string)
cube_file = str(data_path / 'pentacene_HOMO.cube')

# ... or choose URL pointing to cubefile
# cube_file = 'http://143.50.77.12/OrganicMolecule/B3LYP/5A/charge0mult1/5A_MO_73'


# uncomment to create real-space SlicedData
# orbital_slices = SlicedData.init_from_orbital_psi(cube_file,
#                                                  domain='real-space')

# ... or uncomment for k-space SlicedData
orbital_slices = SlicedData.init_from_orbital_psi(cube_file,
                                                  domain='k-space',
                                                  dk3D=0.15,
                                                  E_kin_max=150,
                                                  value='real')

# Plot some slices
fig, _ax = plt.subplots(3, 3)
ax = _ax.flatten()
nplots = len(ax)
nslice = orbital_slices.data.shape[0]

count = 0
for i in range(0, nslice, 1 + nslice // nplots):
    plot_data = orbital_slices.slice_from_index(i)
    ax[count].imshow(plot_data.data)
    count += 1

plt.show()
