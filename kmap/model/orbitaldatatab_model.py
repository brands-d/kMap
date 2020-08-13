import numpy as np
from kmap.library.id import ID
from kmap.library.orbitaldata import OrbitalData


class OrbitalDataTabModel():

    def __init__(self, controller):

        self.controller = controller

        self.displayed_plot_data = None
        self.orbitals = []

    def load_data_from_path(self, path):

        id_ = ID.new_ID()
        new_orbital = OrbitalData.init_from_file(path, ID=id_)
        self.orbitals.append(new_orbital)

        return new_orbital

    def load_data_from_online(self, url, meta_data={}):

        id_ = ID.new_ID()
        new_orbital = OrbitalData.init_from_online(
            url, ID=id_, meta_data=meta_data)

        self.orbitals.append(new_orbital)

        return new_orbital

    def remove_data_by_object(self, orbital):

        self.orbitals.remove(orbital)

    def remove_data_by_index(self, index):

        del self.orbitals[index]

    def update_displayed_plot_data(self):

        aux = []

        for orbital in self.orbitals:

            if self.controller.get_use(orbital.ID):
                # Get all parameters for this orbital
                parameters = self.controller.get_parameters(orbital.ID)
                # Split of first element
                weight, *other = parameters
                # Get scaled kmap
                kmap = weight * orbital.get_kmap(*other)
                aux.append(kmap)

        if aux:
            # Sum kmaps
            self.displayed_plot_data = np.nansum(aux)

        else:
            self.displayed_plot_data = None

        return self.displayed_plot_data

    def remove_orbital_by_ID(self, ID_):

        for orbital in self.orbitals:
            if orbital.ID == ID_:
                self.orbitals.remove(orbital)
                del orbitals
