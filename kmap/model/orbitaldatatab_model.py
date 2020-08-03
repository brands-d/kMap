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

        self.update_displayed_plot_data()

    def load_data_from_online(self, url):

        id_ = ID.new_ID()
        new_orbital = OrbitalData.init_from_online(url, ID=id_)

        self.orbitals.append(new_orbital)

        self.update_displayed_plot_data()

    def remove_data_by_object(self, orbital):

        self.orbitals.remove(orbital)

        self.update_displayed_plot_data()

    def remove_data_by_index(self, index):

        del self.orbitals[index]

        self.update_displayed_plot_data()

    def update_displayed_plot_data(self):

        parameters = self.controller.get_parameters()
        self.displayed_plot_data = np.nansum([orbital.get_kmap(*parameters)
                                              for orbital in self.orbitals])

        return self.displayed_plot_data
