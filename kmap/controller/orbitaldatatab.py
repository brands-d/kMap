# Python Imports
import logging

# Third Party Imports
import h5py
import numpy as np

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
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
UI_file = __directory__ / 'ui/orbitaldatatab.ui'
OrbitalDataTab_UI, _ = uic.loadUiType(UI_file)


class OrbitalDataTab(Tab, OrbitalDataTab_UI):
    orbital_removed = pyqtSignal(int)
    orbital_added = pyqtSignal(int)
    get_energy = pyqtSignal()

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

        return orbital.ID

    def add_orbital_from_online(self, URL, meta_data={}):
        orbital = self.model.load_data_from_online(URL, meta_data)
        self.add_orbital(orbital)

        return orbital.ID

    def get_orbitals(self):
        orbitals = [orbital[0] for orbital in self.model.orbitals]

        return orbitals

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

    def remove_orbital_by_ID(self, ID):
        self.model.remove_orbital_by_ID(ID)

        self.refresh_plot()
        self.mini_3Dkspace_plot.set_orbital(None, ID)
        self.mini_real_plot.set_orbital(None)

        self.orbital_removed.emit(ID)

    def export_to_hdf5(self):
        if not self.interpolation.interpolation_checkbox.isChecked():
            print('Only interpolated OrbitalData can be exported.')
            return

        path = config.get_key('paths', 'hdf5_export_start')
        if path == 'None':
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save .hdf5 File (*.hdf5)')
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, 'Save .hdf5 File (*.hdf5)', str(start_path))

        if not file_name:
            return
        else:
            h5file = h5py.File(file_name, 'w')

        export_energies = eval(config.get_key('orbital', 'export_energies'))
        if isinstance(export_energies, dict):
            export_energies = np.linspace(export_energies['min'],
                                          export_energies['max'],
                                          export_energies['num'],
                                          endpoint=True)

        kmaps = []
        old_energy = self.cube_options.energy_spinbox.value()
        for energy in export_energies:
            self.cube_options.energy_spinbox.setValue(energy)
            kmaps.append(self.get_displayed_plot_data().data)
        self.cube_options.energy_spinbox.setValue(old_energy)
        kmaps = np.array(kmaps)
        xrange, yrange = self.get_displayed_plot_data().range

        h5file.create_dataset('name', data='Orbitals')
        h5file.create_dataset('axis_1_label', data='E_kin')
        h5file.create_dataset('axis_2_label', data='kx')
        h5file.create_dataset('axis_3_label', data='ky')
        h5file.create_dataset('axis_1_units', data='eV')
        h5file.create_dataset('axis_2_units', data='1/Å')
        h5file.create_dataset('axis_3_units', data='1/Å')
        h5file.create_dataset('axis_1_range', data=[export_energies[0],
                                                    export_energies[-1]])
        h5file.create_dataset('axis_2_range', data=xrange)
        h5file.create_dataset('axis_3_range', data=yrange)
        h5file.create_dataset('data', data=kmaps, dtype='f8',
                              compression='gzip', compression_opts=9)
        h5file.close()

    def display_in_matplotlib(self):
        data = self.model.displayed_plot_data
        LUT = self.plot_item.get_LUT()

        window = MatplotlibImageWindow(data, LUT=LUT)

        return window

    def change_kinetic_energy(self, energy):
        self.cube_options.set_kinetic_energy(energy)

    def closeEvent(self, event):
        del self.model

        Tab.closeEvent(self, event)

    def get_plot_labels(self):
        bottom = self.plot_item.get_label('bottom')
        left = self.plot_item.get_label('left')
        return bottom, left

    def save_state(self):
        crosshair_save = self.crosshair.save_state()
        interpolation_save = self.interpolation.save_state()
        polarization_save = self.polarization.save_state()
        cube_options_save = self.cube_options.save_state()
        real_space_options_save = self.real_space_options.save_state()
        colormap_save = self.colormap.save_state()

        orbital_save = []
        for orbital in self.model.orbitals:
            parameters = self.get_parameters(orbital[0].ID)
            use = self.get_use(orbital[0].ID)
            orbital_save.append([*orbital[1:], parameters, use])

        save = {'crosshair': crosshair_save,
                'interpolation': interpolation_save,
                'polarization': polarization_save,
                'cube_options': cube_options_save,
                'real_space_options': real_space_options_save,
                'orbital': orbital_save,
                'colormap': colormap_save,
                'title': self.title}

        return save, []

    def restore_state(self, save):
        ID_maps = []
        for orbital in save['orbital']:
            if orbital[0] == 'path':
                ID = self.add_orbital_from_filepath(orbital[1])

            elif orbital[0] == 'url':
                ID = self.add_orbital_from_online(orbital[1], orbital[2])

            else:
                raise ValueError

            ID_maps.append([orbital[3], ID])
            parameter = [orbital[4][0], *orbital[4][3:6]]
            use = orbital[5]
            self.table.update_orbital_parameters(ID, parameter)
            self.table.update_orbital_use(ID, use)

        crosshair_save = save['crosshair']
        interpolation_save = save['interpolation']
        polarization_save = save['polarization']
        cube_options_save = save['cube_options']
        real_space_options_save = save['real_space_options']
        colormap_save = save['colormap']

        self.crosshair.restore_state(crosshair_save)
        self.interpolation.restore_state(interpolation_save)
        self.polarization.restore_state(polarization_save)
        self.cube_options.restore_state(cube_options_save)
        self.real_space_options.restore_state(real_space_options_save)
        self.colormap.restore_state(colormap_save)

        return ID_maps

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
        x = Axis('kx', '1/Å', [-3, 3], 200)
        y = Axis('ky', '1/Å', [-3, 3], 200)
        self.interpolation.set_label(x, y)
        self.plot_item.set_labels(x, y)

        self.title = 'Orbitals'

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
        self.cube_options.get_match_energy.connect(self.get_energy.emit)

        self.interpolation.smoothing_changed.connect(self.refresh_plot)
        self.interpolation.interpolation_changed.connect(self.refresh_plot)
