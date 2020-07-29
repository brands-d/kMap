# Import the sliced data class from the model folder
from kmap.model.sliceddata import SlicedData
import matplotlib.pyplot as plt
import os

# Get path to the directory this file is in
dir_path, __ = os.path.split(os.path.realpath(__file__))
file_path = dir_path + '/basic.hdf5'
# Loading from file (Initialisation methods are usually class members)
sliced_data = SlicedData.init_from_hdf5(file_path)

# Print stored meta_data
print(sliced_data.meta_data)
print(sliced_data.slice_keys)

# Get a PlotData object consisting of the 0th slice and it's axes
plot_data = sliced_data.slice_from_idx(0)

# Alternatively get the slice with a slice key (certain energy or time
# for example)
plot_data = sliced_data.slice_from_key(2)

# Plot
__, axes = plt.subplots()
axes.imshow(plot_data.data)
plt.show()
