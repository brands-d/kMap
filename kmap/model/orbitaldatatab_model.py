import numpy as np

from kmap.library.id import ID as IDD
from kmap.library.orbitaldata import OrbitalData


class OrbitalDataTabModel:
    def __init__(self, controller):
        self.controller = controller

        self.displayed_plot_data = None
        self.orbitals = []

    def load_data_from_path(self, path, ID=None):
        if ID is None:
            id_ = IDD.new_ID()

        else:
            id_ = ID
            IDD.update(id_)

        new_orbital = OrbitalData.init_from_file(path, ID=id_)
        self.orbitals.append([new_orbital, "path", path, None, id_])

        return new_orbital

    def load_data_from_online(self, url, meta_data={}, ID=None):
        if ID is None:
            id_ = IDD.new_ID()

        else:
            id_ = ID
            IDD.update(id_)

        new_orbital = OrbitalData.init_from_online(url, ID=id_, meta_data=meta_data)

        self.orbitals.append([new_orbital, "url", url, meta_data, id_])

        return new_orbital

    def remove_data_by_object(self, orbital):
        index = [orb[0] for orb in self.orbitals].index(orbital)

        self.remove_data_by_index(index)

    def remove_data_by_index(self, index):
        del self.orbitals[index]

    def get_orbital_kmap_by_ID(self, ID):
        orbital = self.ID_to_orbital(ID)
        if orbital is None:
            raise IndexError("wrong ID")

        parameters = self.controller.get_parameters(ID)

        # Split of first element
        weight, *other = parameters
        # Get scaled kmap
        kmap = weight * orbital.get_kmap(*other)

        return kmap

    def update_displayed_plot_data(self):
        kmaps = []

        for orbital in self.orbitals:
            ID = orbital[0].ID

            if self.controller.get_use(ID):
                # Get all parameters for this orbital
                kmap = self.get_orbital_kmap_by_ID(ID)
                kmaps.append(kmap)

        if kmaps:
            # Sum kmaps
            self.displayed_plot_data = np.nansum(kmaps)

        else:
            self.displayed_plot_data = None

        return self.displayed_plot_data

    def remove_orbital_by_ID(self, ID):
        orbital = self.ID_to_orbital(ID)

        if orbital is not None:
            self.remove_data_by_object(orbital)

    def ID_to_orbital(self, ID):
        for orbital in self.orbitals:
            if orbital[0].ID == ID:
                return orbital[0]

        return None
