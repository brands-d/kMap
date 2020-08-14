from kmap.library.id import ID
from kmap.library.sliceddata import SlicedData


class SlicedDataTabModel():

    def __init__(self, path, delayed_access=False):

        self.path = path
        self.data = None
        self.displayed_plot_data = None

        # For later use
        self.delayed_access = delayed_access

        self.load_data_from_path(path)

    def load_data_from_path(self, path):

        self.data = SlicedData.init_from_hdf5(path,)

        self.change_slice(0, 0)

    def change_slice(self, index, axis):

        self.displayed_plot_data = self.data.slice_from_index(index, axis)

        return self.displayed_plot_data

    def to_string(self):

        rep = 'Path:\t%s\n%s' % (self.path, str(self.data))

        return rep