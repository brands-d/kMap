import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

# How to load sliced data
with np.load(data_path / 'example8_sliceddata.npz', allow_pickle=True) as f:
    axis_1 = f['axis_1'] # first axis are the slices
    axis_2 = f['axis_2']
    axis_3 = f['axis_3']
    slices = f['slices'] # 3D numpy array: axis order corresponds to names

# WARNING: Matplotlib imshow needs origin lower to display correctly!
plt.imshow(slices[14], origin='lower', extent=[axis_2[0], axis_2[-1], axis_3[0], axis_3[-1]])


# How to load orbital data & splitview data
with np.load(data_path / 'example8_orbitaldata.npz', allow_pickle=True) as f:
    axis_1 = f['axis_1']
    axis_2 = f['axis_2']
    data = f['data']

plt.figure()
plt.imshow(data, origin='lower', extent=[axis_1[0], axis_1[-1], axis_2[0], axis_2[-1]])


# How to load profile plot data
with np.load(data_path / 'example8_profiledata.npz', allow_pickle=True) as f:
    data = f['data'] # first index is the data set, second index are x,y

plt.figure()
plt.plot(data[0][0], data[0][1]) # first line
plt.plot(data[1][0], data[1][1]) # second line
plt.show()
