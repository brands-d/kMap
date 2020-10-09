# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.sliceddata import SlicedData

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

# Import the sliced data class from the model folder

# Get path to the directory this file is in
# ATTENTION FILE DOES NOT EXIT ANYMORE
file_path = str(data_path / 'example5_6584.hdf5')

# Loading from file (Initialisation methods are usually class members)
sliced_data = SlicedData.init_from_hdf5(file_path)

# Get a PlotData object consisting of the 10th slice and its axes
plot_data = sliced_data.slice_from_index(10)


# Plot
__, axes = plt.subplots()
axes.imshow(plot_data.data)
plt.show()
