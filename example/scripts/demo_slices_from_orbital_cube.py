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
data_path = Path(__file__).parent / Path('../data/')

# choose local path to cube-file (string because init at line 31 expects
# a string)
cube_file = str(data_path / 'pentacene_HOMO.cube')

# ... or choose URL pointing to cubefile
#cube_file = 'http://143.50.77.12/OrganicMolecule/B3LYP/5A/charge0mult1/5A_MO_73'


# Create SlicedData object
orbital  = [[cube_file,{}]]
name = '5A HOMO'
parameters =['k-space', # either 'real-space' or 'k-space'
             0.15,         # desired resolution for 3D-Fourier-Transform.
             150,          # maximum kinetic energy in eV
             'real']       # choose between 'real', 'imag', 'abs' or 'abs2'
                           #   for Re(), Im(), |..| or |..|^2

orbital_slices = SlicedData.init_from_orbital_cube(name,orbital,parameters)

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
