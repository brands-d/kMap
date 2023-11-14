import logging
import os
from pathlib import Path

from kmap.config.config import config
from kmap.library.sliceddata import SlicedData


class SlicedDataTabModel:
    def __init__(self):
        self.data = None
        self.load_data = None
        self.symmetry = ["no", False]

    def load_data_from_URLs(self, URLs, ID=None):  # -> create data[BE,kx,ky]
        # Last element in URLs are the parameters. All other elements
        # are individual orbitals to load. Each is a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbitals, options = URLs
        name, *parameters = options
        s_share = float(config.get_key("orbital", "s_share_sliced"))

        self.data = SlicedData.init_from_orbitals(
            name, orbitals, parameters, s_share=s_share, ID=ID
        )
        self.load_data = ["load_from_URLs", URLs]

        self.change_slice(0, 0)

    def load_data_from_URL(self, URL, ID=None):  # -> create data[photon_energy,kx,ky]
        # Last element in URL are the parameters. The first element
        # is the orbital to load as a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbital, options = URL
        name, *parameters = options
        s_share = float(config.get_key("orbital", "s_share_sliced"))

        self.data = SlicedData.init_from_orbital_photonenergy(
            name, orbital, parameters, s_share=s_share, ID=ID
        )
        self.load_data = ["load_from_URL", URL]

        self.change_slice(0, 0)

    def load_data_from_cube(self, URL, ID=None):  # -> create either psi[x,y,z]
        #               or psik[kx,ky,kz]

        # Last element in URL are the parameters. The first element
        # is the orbital to load as a list of length 2
        # with first entry being the URL, the second the meta_data
        # dictionary
        *orbital, options = URL
        name, *parameters = options
        self.data = SlicedData.init_from_orbital_cube(name, orbital, parameters, ID)
        self.load_data = ["load_from_cube", URL]

        self.change_slice(0, 0)

    def load_data_from_path(self, path, ID=None):
        log = logging.getLogger("kmap")
        possible_paths = [path]
        file_name = Path(path).name
        possible_paths.append(Path(config.get_key("paths", "hdf5_start")) / file_name)
        for path in config.get_key("paths", "path").split(","):
            possible_paths.append(Path(path) / file_name)

        for path in possible_paths:
            log.info(f"Looking for {file_name} in {path}.")
            if os.path.isfile(path):
                log.info(f"Found.")
                self.data = SlicedData.init_from_hdf5(path, ID=ID)
                self.load_data = ["load_from_path", path]
                self.change_slice(0, 0)

                return
            else:
                continue

        # No path worked
        print(
            f"ERROR: File {file_name} wasn't found. Please add its location to the search path (general_settings.paths.path"
        )

    def save_state(self):
        load_type, load_args = self.load_data
        save = {"load_type": load_type, "load_args": load_args, "ID": self.data.ID}

        return save

    def restore_state(self, save):
        if save["load_type"] == "load_from_path":
            self.load_data_from_path(save["load_args"], save["ID"])

        elif save["load_type"] == "load_from_cube":
            self.load_data_from_cube(save["load_args"], save["ID"])

        elif save["load_type"] == "load_from_URL":
            self.load_data_from_URL(save["load_args"], save["ID"])

        else:
            self.load_data_from_URLs(save["load_args"], save["ID"])

    def transpose(self, axis_order):
        self.data.transpose(axis_order)

    def change_symmetry(self, symmetry, mirror):
        self.symmetry = [symmetry, mirror]

    def change_slice(self, index, axis):
        self.displayed_plot_data = self.data.slice_from_index(index, axis)
        self.displayed_plot_data.symmetrise(*self.symmetry)

        return self.displayed_plot_data

    def to_string(self):
        rep = "%s" % str(self.data)

        return rep
