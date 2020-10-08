# Third Party Imports
import h5py
import numpy as np

# this script demonstrates the file format of hdf5-files for "Sliced Data" Objects
# Note that equidistant grids in x, y and z-directions are assumed. The grid spacing
# may, however, be different along the three axes. 

# create some arbitrary demo data
x       = np.linspace(-3,3,80)
y       = np.linspace(-2,4,60)
z       = np.linspace(-1,2,50)
X, Y, Z = np.meshgrid(x,y,z, indexing='xy')
data    = np.sin(X*Y)*np.exp(-(X**2 + Y**2 + Z**2)) # some arbitrary function of x, y, z
                                                    # used to create the 3D numpy array 'data'

# now write data and axis to hdf5-file
h5file = h5py.File('name_of_my_file.hdf5','w')  # create new file

# absolutlely necessary datasets are the following
h5file.create_dataset('name',data='name of my dataset')

h5file.create_dataset('axis_1_label',data='x') # label for x-axis (str)
h5file.create_dataset('axis_2_label',data='y') # label for y-axis (str)
h5file.create_dataset('axis_3_label',data='z') # label for z-axis (str)

h5file.create_dataset('axis_1_units',data='-') # physical units for x-axis (str)
h5file.create_dataset('axis_2_units',data='-') # physical units for x-axis (str)
h5file.create_dataset('axis_3_units',data='-') # physical units for x-axis (str)

h5file.create_dataset('axis_1_range',data=[x[0], x[-1]]) # axis-1 range:  [float, float]
h5file.create_dataset('axis_2_range',data=[y[0], y[-1]]) # axis-2 range:  [float, float]
h5file.create_dataset('axis_3_range',data=[z[0], z[-1]]) # axis-3 range:  [float, float]

h5file.create_dataset('data',data=data,     #  write 3D-numpy-array
                       dtype='f8',          # 'f8' = double precision, 'f4' = single precision
                       compression='gzip', compression_opts=9)  # these options turn on data compression if needed


# optionally meta-data information about the data can be provided
h5file.create_dataset('alias',data='shortname') # an alternative, short name for the dataset

# further information about the data set is provided here as the Python dictionary 'meta_data'
meta_data = {'parameter1':1.23,          # some number
             'list1'     :[1, 2, 3],     # some list
             'string1'   :'more info'}   # some string
for key in meta_data:
    h5file.create_dataset(key,data=meta_data[key])


# close hdf5-file
h5file.close()


