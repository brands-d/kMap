from kmap.library.id import ID
from kmap.library.sliceddata import SlicedData


class SlicedDataTabModel():

    def __init__(self):

        self.data = None

    def load_data_from_URLs(self, URLs):

        # Last element in URLs are the parameters. All other elements
        # are individual orbitals to load. Each is a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbitals, options = URLs
        name, *parameters = options
        self.data = SlicedData.init_from_orbitals(name, orbitals, parameters)

        self.change_slice(0, 0)

    def load_data_from_path(self, path):

        self.data = SlicedData.init_from_hdf5(path)

        self.change_slice(0, 0)

    def change_slice(self, index, axis):

        self.displayed_plot_data = self.data.slice_from_index(index, axis)

        return self.displayed_plot_data

    def to_string(self):

        rep = '%s' % str(self.data)

        return rep
