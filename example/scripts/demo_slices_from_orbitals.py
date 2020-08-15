# Python imports
import os
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath(__file__)) + '/../data/'

# kmap imports
from kmap.library.database import Database
from kmap.library.sliceddata import SlicedData
# 
db = Database(path + 'molecules.txt')
molecule = db.get_molecule_by_ID(11)  # choose pentacene molecule for testing ...

# ... and for testing choose some subset of orbitals of pentacene
name       = molecule.full_name   # set name for SlicedData Object
kmap_stack = SlicedData.init_from_orbitals(name,molecule.orbitals[6:-4],
                                           photon_energy=40,fermi_energy=-3)  


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

