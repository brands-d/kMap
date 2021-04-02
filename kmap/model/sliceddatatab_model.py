from kmap.library.id import ID
from kmap.library.sliceddata import SlicedData
from kmap.library.misc import transpose_axis_order
from kmap.config.config import config


class SlicedDataTabModel():

    def __init__(self):
        self.data = None
        self.load_data = None
        self.symmetry = ['no', False]

    def load_data_from_URLs(self, URLs):  # -> create data[BE,kx,ky]

        # Last element in URLs are the parameters. All other elements
        # are individual orbitals to load. Each is a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbitals, options = URLs
        name, *parameters = options
        s_share = float(config.get_key('orbital', 's_share'))

        self.data = SlicedData.init_from_orbitals(name, orbitals,
                                                  parameters, s_share=s_share)
        self.load_data = ['load_from_URLs', URLs]

        self.change_slice(0, 0)

    def load_data_from_URL(self, URL):  # -> create data[photon_energy,kx,ky]

        # Last element in URL are the parameters. The first element
        # is the orbital to load as a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbital, options = URL
        name, *parameters = options
        s_share = float(config.get_key('orbital', 's_share'))

        self.data = SlicedData.init_from_orbital_photonenergy(
            name, orbital, parameters, s_share=s_share)
        self.load_data = ['load_from_URL', URL]

        self.change_slice(0, 0)

    def load_data_from_cube(self, URL):  # -> create either psi[x,y,z]
        #               or psik[kx,ky,kz]

        # Last element in URL are the parameters. The first element
        # is the orbital to load as a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbital, options = URL
        name, *parameters = options
        self.data = SlicedData.init_from_orbital_cube(
            name, orbital, parameters)
        self.load_data = ['load_from_cube', URL]

        self.change_slice(0, 0)

    def load_data_from_path(self, path):
        self.data = SlicedData.init_from_hdf5(path)
        self.load_data = ['load_from_path', path]

        self.change_slice(0, 0)

    def save_state(self):
        load_type, load_args = self.load_data
        save = {'load_type': load_type,
                'load_args': load_args, 'ID': self.data.ID}

        return save

    def transpose(self, constant_axis):
        axis_order = transpose_axis_order(constant_axis)

        self.data.transpose(axis_order)

    def change_symmetry(self, symmetry, mirror):
        self.symmetry = [symmetry, mirror]

    def change_slice(self, index, axis):
        self.displayed_plot_data = self.data.slice_from_index(index, axis)
        self.displayed_plot_data.symmetrise(*self.symmetry)

        return self.displayed_plot_data

    def to_string(self):
        rep = '%s' % str(self.data)

        return rep
