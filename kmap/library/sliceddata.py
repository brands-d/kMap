# Python Imports
import h5py
import numpy as np

# Own Imports
from kmap.library.id import ID
from kmap.library.plotdata import PlotData
from kmap.library.abstractdata import AbstractData
from kmap.library.misc import axis_from_range


class SlicedData(AbstractData):

    def __init__(self, name, axis_1, axis_2, axis_3, data, meta_data={}):

        if isinstance(name, str) and name:
            super(SlicedData, self).__init__(ID.new_ID(), name, meta_data)

        else:
            raise ValueError('name has to be string and not empty')

        data = np.array(data, dtype=np.float64)
        if len(data.shape) == 3:
            self.data = data

        else:
            raise ValueError('data has to be 3D')

        axis_1 = Axis.init_from_hdf_list(axis_1, len(data[:, 0, 0]))
        axis_2 = Axis.init_from_hdf_list(axis_2, len(data[0, :, 0]))
        axis_3 = Axis.init_from_hdf_list(axis_3, len(data[0, 0, :]))
        self.axes = [axis_1, axis_2, axis_3]

    @classmethod
    def init_from_hdf5(cls, file_path, keys={}, meta_data={}):

        # Updates default file_keys with user defined keys
        file_keys = {'name': 'name', 'axis_1_label': 'axis_1_label',
                     'axis_1_units': 'axis_1_units',
                     'axis_1_range': 'axis_1_range',
                     'axis_2_label': 'axis_2_label',
                     'axis_2_units': 'axis_2_units',
                     'axis_2_range': 'axis_2_range',
                     'axis_3_label': 'axis_3_label',
                     'axis_3_units': 'axis_3_units',
                     'axis_3_range': 'axis_3_range',
                     'data': 'data'}
        file_keys.update(keys)

        with h5py.File(file_path, 'r') as file:

            # First check if necessary datasets exist
            for _, value in file_keys.items():
                if value not in file:
                    raise AttributeError('Dataset is missing %s' % value)

            # Read all datasets
            for key, value in file.items():
                if key == file_keys['name']:
                    name = str(file[key][()])

                elif key == file_keys['axis_1_label']:
                    axis_1_label = file[key][()]

                elif key == file_keys['axis_2_label']:
                    axis_2_label = file[key][()]

                elif key == file_keys['axis_3_label']:
                    axis_3_label = file[key][()]

                elif key == file_keys['axis_1_units']:
                    axis_1_units = file[key][()]

                elif key == file_keys['axis_2_units']:
                    axis_2_units = file[key][()]

                elif key == file_keys['axis_3_units']:
                    axis_3_units = file[key][()]

                elif key == file_keys['axis_1_range']:
                    axis_1_range = file[key][()]

                elif key == file_keys['axis_2_range']:
                    axis_2_range = file[key][()]

                elif key == file_keys['axis_3_range']:
                    axis_3_range = file[key][()]

                elif key == file_keys['data']:
                    data = file[key][()]

                else:
                    meta_data.update({key: str(f[key][()])})

        axis_1 = [axis_1_label, axis_1_units, axis_1_range]
        axis_2 = [axis_2_label, axis_2_units, axis_2_range]
        axis_3 = [axis_3_label, axis_3_units, axis_3_range]

        return cls(name, axis_1, axis_2, axis_3, data, meta_data)

    def slice_from_index(self, index, axis=0):

        if axis == 0:
            data = self.data[index, :, :]
            range_ = [self.axes[1].range, self.axes[2].range]

        elif axis == 1:
            data = self.data[:, index, :]
            range_ = [self.axes[0].range, self.axes[2].range]

        elif axis == 2:
            data = self.data[:, :, index]
            range_ = [self.axes[0].range, self.axes[1].range]

        else:
            raise ValueError('axis has to be between 1 and 3')

        return PlotData(data, range_)


class Axis():

    def __init__(self, label, units, range_, num):

        self.label = label
        self.units = units
        self.range = range_
        self.axis = axis_from_range(range_, num)

    @classmethod
    def init_from_hdf_list(cls, axis, num):

        if Axis._is_correct_axis(axis):
            return cls(*axis, num)

    @classmethod
    def _is_correct_axis(self, axis):

        if not isinstance(axis, list) or len(axis) != 3:
            raise ValueError('axis has to be a list of length 3')

        label, units, range_ = axis
        if not isinstance(label, str) or not label:
            raise ValueError('axis label has to be a non empty string')

        if not isinstance(units, str) or not units:
            raise ValueError('axis units has to be a non empty string')

        if len(range_) != 2:
            raise ValueError('axis range has to be list of length 2')

        minimum, maximum = range_
        if not np.isfinite(minimum) or not np.isfinite(maximum):
            raise ValueError('axis range can not contain inf or nan values')

        if not minimum < maximum:
            raise ValueError(
                'axis minimum has to strictly smaller than maxmimum')

        return True
