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

        id_ = ID.new_ID()
        self.data = SlicedData.init_from_hdf5(path, ID=id_)

        self.change_slice(0)

    def change_slice(self, index):

        self.displayed_plot_data = self.data.slice_from_idx(index)

        return self.displayed_plot_data
