# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QDir

# Own Imports
from kmap import __directory__
from kmap.library.misc import get_ID_from_tab_text
from kmap.library.qwidgetsub import Tab
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibWindow
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.colormap import Colormap
from kmap.controller.cubeoptions import CubeOptions
from kmap.controller.orbitaltable import OrbitalTable
from kmap.controller.interpolation import Interpolation
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.polarization import Polarization
from kmap.library.sliceddata import Axis
from kmap.config.config import config


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/orbitaldatatab.ui')
OrbitalDataTab_UI, _ = uic.loadUiType(UI_file)


class OrbitalDataTab(Tab, OrbitalDataTab_UI):

    orbital_removed = pyqtSignal(int)
    orbital_added = pyqtSignal(int)

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

        self.orbital_added.emit(orbital.ID)

    def refresh_plot(self):

        data = self.model.update_displayed_plot_data()

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.plot_item.plot(data)

    def refresh_mini_plots(self, ID, orbital_changed=True):

        data = self.model.get_orbital_kmap_by_ID(ID)
        parameters = self.get_parameters(ID)
        phi, theta, psi = parameters[3:6]
        E_kin = parameters[1]

        if orbital_changed:
            orbital = self.model.ID_to_orbital(ID)
            self.mini_3Dkspace_plot.set_orbital(orbital, ID)
            self.mini_real_plot.set_orbital(orbital)

        self.mini_3Dkspace_plot.change_energy(E_kin)
        self.mini_3Dkspace_plot.rotate_orbital(phi, theta, psi)
        self.mini_real_plot.rotate_orbital(phi, theta, psi)

    def refresh_mini_plot_polarization(self):

        polarization, alpha, beta = self.polarization.get_parameters()[1:4]

        self.mini_real_plot.rotate_photon(polarization, alpha, beta)

    def get_crosshair(self):

        return self.crosshair

    def get_parameters(self, ID):

        kinetic_energy, dk, symmetry = self.cube_options.get_parameters()
        parameters = self.table.get_parameters_by_ID(ID)
        weight, *orientation = parameters
        polarization = self.polarization.get_parameters()

        return (weight, kinetic_energy, dk,
                *orientation, *polarization, symmetry)

    def get_use(self, ID):

        return self.table.get_use_by_ID(ID)

    def get_displayed_plot_data(self):

        return self.model.displayed_plot_data

    def crosshair_changed(self):

        self.crosshair.update_label()

    def change_parameter(self):

        self.refresh_plot()

        ID = self.mini_3Dkspace_plot.ID
        if ID is not None:
            self.refresh_mini_plots(ID, orbital_changed=False)

    def orbitals_changed(self, ID):

        self.refresh_plot()

        current_ID = self.mini_3Dkspace_plot.ID
        if current_ID is None or current_ID == ID:
            self.refresh_mini_plots(ID, orbital_changed=False)

    def get_title(self):

        return 'Orbitals'

    def remove_orbital_by_ID(self, ID):

        orbital = self.model.remove_orbital_by_ID(ID)

        self.refresh_plot()
        self.mini_3Dkspace_plot.set_orbital(None, ID)
        self.mini_real_plot.set_orbital(None)

        self.orbital_removed.emit(ID)

    def display_in_matplotlib(self):

        data = self.model.displayed_plot_data
        LUT = self.plot_item.get_LUT()

        self.window = MatplotlibWindow(data, LUT=LUT)

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def get_plot_labels(self):

        bottom = self.plot_item.get_label('bottom')
        left = self.plot_item.get_label('left')
        return bottom, left

    def _setup(self):

        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap([self.plot_item])
        self.interpolation = Interpolation()

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(4, self.interpolation)
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(5, self.crosshair)

        self.mini_real_plot.set_options(self.real_space_options)
        self.mini_3Dkspace_plot.set_options(self.real_space_options)

        # Rough axis values for all orbitals to set labels for interpolation
        x = Axis('kx', '1/A', [-3, 3], 200)
        y = Axis('ky', '1/A', [-3, 3], 200)
        self.interpolation.set_label(x, y)
        self.plot_item.set_label(x, y)

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.table.orbital_changed.connect(self.orbitals_changed)
        self.table.orbital_removed.connect(self.remove_orbital_by_ID)
        self.table.orbital_selected.connect(self.refresh_mini_plots)
        self.polarization.polarization_changed.connect(
            self.change_parameter)
        self.polarization.polarization_changed.connect(
            self.refresh_mini_plot_polarization)
        self.cube_options.symmetrization_changed.connect(
            self.change_parameter)
        self.cube_options.energy_changed.connect(
            self.change_parameter)
        self.cube_options.resolution_changed.connect(
            self.change_parameter)

        self.interpolation.smoothing_changed.connect(self.refresh_plot)
        self.interpolation.interpolation_changed.connect(self.refresh_plot)
