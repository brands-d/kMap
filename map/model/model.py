from map.model.sliceddata import SlicedData


class Model():

    def __init__(self):

        self.loaded_sliced_data = []

    def load_sliced_data_from_filepath(self, path):

        self.loaded_sliced_data.append(SlicedData.init_from_hdf5(path))
