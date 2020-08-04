import logging
from PyQt5.QtWidgets import QWidget
from kmap.library.misc import get_ID_from_tab_text
from kmap.ui.orbitaldatatab_ui import OrbitalDataTabUI
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.config.config import config


class OrbitalDataTab(OrbitalDataTabUI):

    def __init__(self):

        self.model = OrbitalDataTabModel(self)

        OrbitalDataTabUI.__init__(self)

    def add_orbital_from_filepath(self, path):

        orbital = self.model.load_data_from_path(path)

        self.table.add_orbital(orbital)
        self.refresh_plot()

    def refresh_plot(self):

        data = self.model.update_displayed_plot_data()

        self.plot_item.plot(data)

    def get_parameters(self):

        kinetic_energy = 30
        dk = 0.03
        #orientation = self.orientation.get_parameters()
        orientation = [0, 0, 0]
        polarization = self.polarization.get_parameters()

        return (kinetic_energy, dk, *orientation, *polarization)

    def _get_orientation(self):

        phi = 0
        theta = 0
        psi = 0

        return phi, theta, psi

    def crosshair_changed(self):

        data = self.model.displayed_plot_data
        self.crosshair.update_label()

    def polarization_changed(self):

        self.refresh_plot()

    def get_title(self):

        return 'Gas Phase Simulation'
