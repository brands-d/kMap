# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic

# Own Imports
from kmap import __directory__
from kmap.library.misc import get_ID_from_tab_text
from kmap.library.qwidgetsub import Tab
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.colormap import Colormap
from kmap.controller.orbitaltable import OrbitalTable
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.polarization import Polarization
from kmap.config.config import config


# Load .ui File
UI_file = __directory__ + '/ui/orbitaldatatab.ui'
OrbitalDataTab_UI, _ = uic.loadUiType(UI_file)


class OrbitalDataTab(Tab, OrbitalDataTab_UI):

    def __init__(self):

        # Setup GUI
        super(OrbitalDataTab, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.model = OrbitalDataTabModel(self)

    def add_orbital_from_filepath(self, path):

        orbital = self.model.load_data_from_path(path)
        self.add_orbital(orbital)

    def add_orbital_from_online(self, URL, meta_data={}):

        orbital = self.model.load_data_from_online(URL, meta_data)
        self.add_orbital(orbital)

    def add_orbital(self, orbital):

        if 'orientation' in orbital.meta_data:
            orientation = orbital.meta_data['orientation']

        else:
            orientation = 'xy'

        self.table.add_orbital(orbital, orientation)

        self.refresh_plot()

    def refresh_plot(self):

        data = self.model.update_displayed_plot_data()

        self.plot_item.plot(data)

    def get_parameters(self, ID):

        # Hardcoded for now
        kinetic_energy = 30
        dk = 0.03

        parameters = self.table.get_parameters_by_ID(ID)
        weight, *orientation = parameters
        *polarization, symmetry = self.polarization.get_parameters()
        
        return (weight, kinetic_energy, dk,
                *orientation, *polarization, symmetry)

    def get_use(self, ID):

        return self.table.get_use_by_ID(ID)

    def crosshair_changed(self):

        data = self.model.displayed_plot_data
        self.crosshair.update_label()

    def polarization_changed(self):

        self.refresh_plot()

    def orbitals_changed(self):

        self.refresh_plot()

    def get_title(self):

        return 'Gas Phase Simulation'

    def remove_orbital_by_ID(self, ID):

        orbital = self.model.remove_orbital_by_ID(ID)

        self.refresh_plot()

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def _setup(self):

        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap(self.plot_item)

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.table.orbital_changed.connect(self.orbitals_changed)
        self.table.orbital_removed.connect(self.remove_orbital_by_ID)
        self.polarization.polarization_changed.connect(
            self.polarization_changed)
        self.polarization.symmetrization_changed.connect(
            self.polarization_changed)
