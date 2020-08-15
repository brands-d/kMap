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


# Get a PlotData object consisting of the 10th slice and its axes
plot_data = kmap_stack.slice_from_index(10)

# Plot
__, axes = plt.subplots()
axes.imshow(plot_data.data)
plt.show()

