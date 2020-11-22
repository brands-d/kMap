# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ / 'ui/realplotoptions.ui'
RealPlotOptions_UI, _ = uic.loadUiType(UI_file)


class RealPlotOptions(QWidget, RealPlotOptions_UI):
    set_camera = pyqtSignal(int, int, int)
    show_grid_changed = pyqtSignal(int)
    show_mesh_changed = pyqtSignal(int)
    show_bonds_changed = pyqtSignal(int)
    show_photon_changed = pyqtSignal(int)
    show_hemisphere_changed = pyqtSignal(int)
    iso_val_changed = pyqtSignal()

    def __init__(self, plot_item):
        # Setup GUI
        super(RealPlotOptions, self).__init__()
        self.setupUi(self)
        self._connect()

    def save_state(self):
        iso_val = self.get_iso_val()
        checkboxes = [self.show_grid_checkbox,
                      self.show_isosurface_checkbox,
                      self.show_bond_checkbox,
                      self.show_photon_checkbox,
                      self.show_hemisphere_checkbox]
        booleans = [checkbox.checkState() for checkbox in checkboxes]

        save = {'iso_val': iso_val, 'booleans': booleans}

        return save

    def restore_state(self, save):
        iso_val = save['iso_val']
        self.iso_spinbox.setValue(iso_val)

        checkboxes = [self.show_grid_checkbox,
                      self.show_isosurface_checkbox,
                      self.show_bond_checkbox,
                      self.show_photon_checkbox,
                      self.show_hemisphere_checkbox]
        for checkbox, state in zip(checkboxes, save['booleans']):
            checkbox.setCheckState(state)

    def reset_camera(self):
        distance = 75
        elevation = 90
        azimuth = -90
        self.set_camera.emit(distance, elevation, azimuth)

    def is_show_grid(self):
        return self.show_grid_checkbox.isChecked()

    def is_show_bonds(self):
        return self.show_bond_checkbox.isChecked()

    def is_show_hemisphere(self):
        return self.show_hemisphere_checkbox.isChecked()

    def is_show_photon(self):
        return self.show_photon_checkbox.isChecked()

    def is_show_mesh(self):
        return self.show_isosurface_checkbox.isChecked()

    def get_iso_val(self):
        return self.iso_spinbox.value()

    def _change_bonds_show(self, state):
        self.show_bonds_changed.emit(state)

    def _change_photon_show(self, state):
        self.show_photon_changed.emit(state)

    def _change_grid_show(self, state):
        self.show_grid_changed.emit(state)

    def _change_mesh_show(self, state):
        self.show_mesh_changed.emit(state)

    def _change_hemisphere_show(self, state):
        self.show_hemisphere_changed.emit(state)

    def _change_iso_val(self):
        self.iso_val_changed.emit()

    def _connect(self):
        self.reset_camera_button.clicked.connect(self.reset_camera)
        self.show_bond_checkbox.stateChanged.connect(self._change_bonds_show)
        self.show_photon_checkbox.stateChanged.connect(
            self._change_photon_show)
        self.show_grid_checkbox.stateChanged.connect(self._change_grid_show)
        self.show_hemisphere_checkbox.stateChanged.connect(
            self._change_hemisphere_show)
        self.show_isosurface_checkbox.stateChanged.connect(
            self._change_mesh_show)
        self.iso_spinbox.valueChanged.connect(self._change_iso_val)
