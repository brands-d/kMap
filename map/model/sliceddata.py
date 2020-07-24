import h5py
import numpy as np
from abc import ABCMeta, abstractmethod
from map.model.plotdata import PlotData


class AbstractSlicedData(metaclass=ABCMeta):

    def __init__(self, slice_keys, ID, name, meta_data):

        # Test for uniqueness in the slice_axis key list
        if len(slice_keys) > len(set(slice_keys)):
            raise ValueError('slice_axis has to have only unique values')
        else:
            self.slice_keys = slice_keys

        self.name = name
        self.ID = ID
        self.meta_data = meta_data

    @abstractmethod
    def slice_from_idx(self, idx):
        pass

    @abstractmethod
    def slice_from_key(self, key):
        pass


class SlicedData(AbstractSlicedData):

    def __init__(self, slices, ranges, slice_keys, ID, name='', meta_data={}):

        # Test if slice_keys matches slices
        if len(slice_keys) != len(slices):
            raise TypeError('slice_axis has to be the same length as slices')

        super().__init__(slice_keys, ID, name, meta_data)

        # If only one range is supplied, it applies to all slices
        if len(np.array(ranges).shape) == 2:
            self._slices = [PlotData(slice_, ranges) for slice_ in slices]

        # Each slices has its own range
        elif len(ranges) == len(slices):
            self._slices = [PlotData(slice_, range_)
                            for slice_, range_ in zip(slices, ranges)]
        else:
            raise TypeError(
                'range_ needs to be specified either once for all or for all' +
                'slices individually')

    @classmethod
    def init_from_hdf5(cls, file_path, ID, keys={}):

        # Updates default file_keys with user defined keys
        file_keys = {'name': 'name', 'slice_keys': 'slice_keys',
                     'slices': 'slices', 'range': 'range'}
        file_keys.update(keys)

        meta_data = {}

        with h5py.File(file_path, 'r') as f:

            # First check if necessary datasets exist
            if (file_keys['name'] not in f or
                file_keys['slice_keys'] not in f or
                    file_keys['range'] not in f):
                raise AttributeError('Necessary dataset in hdf5 file missing')

            # Read all datasets
            for key, value in f.items():
                if key == file_keys['name']:
                    name = str(f[key][()])

                elif key == file_keys['slice_keys']:
                    slice_keys = f[key][()]

                elif key == file_keys['slices']:
                    slices = f[key][()]

                elif key == file_keys['range']:
                    ranges = f[key][()]

                else:
                    meta_data.update({key: str(f[key][()])})

        return cls(slices, ranges, slice_keys, ID, name=name,
                   meta_data=meta_data)

    def slice_from_idx(self, idx):

        return self._slices[idx]

    def slice_from_key(self, key):

        try:
            idx = self.slice_keys.index(key)
            return self._slices[idx]

        except ValueError:
            return None
