from pathlib import Path

import h5py
import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog

from kmap import __directory__
from kmap.config.config import config
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.interpolation import Interpolation
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
from kmap.library.qwidgetsub import Tab
from kmap.library.sliceddata import Axis
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.ui.orbitaldatatab import Ui_orbitaldatatab as OrbitalDataTab_UI


class OrbitalDataTab(Tab, OrbitalDataTab_UI):
    orbital_removed = Signal(int)
    orbital_added = Signal(int)
    get_energy = Signal()

    def __init__(self):
        # Setup GUI
        super(OrbitalDataTab, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.model = OrbitalDataTabModel(self)

    @classmethod
    def init_from_save(cls, save, dependencies, tab_widget=None):
        self = cls()

        for orbital in save["orbitals"]:
            if orbital["load_type"] == "path":
                self.add_orbital_from_filepath(orbital["load_args"], orbital["ID"])

            elif orbital["load_type"] == "url":
                self.add_orbital_from_online(
                    orbital["load_args"],
                    meta_data=orbital["meta_data"],
                    ID=orbital["ID"],
                )

        self.interpolation.restore_state(save["interpolation"])
        self.table.restore_state(save["table"])
        self.polarization.restore_state(save["polarization"])
        self.cube_options.restore_state(save["cube_options"])
        self.real_space_options.restore_state(save["real_space_options"])
        self.crosshair.restore_state(save["crosshair"])
        self.colormap.restore_state(save["colormap"])
        self.plot_item.set_levels(save["levels"])
        self.plot_item.set_colormap(save["colorscale"])

        return self

    def add_orbital_from_filepath(self, path, ID=None):
        orbital = self.model.load_data_from_path(path, ID=ID)
        self.add_orbital(orbital)

        return orbital.ID

    def add_orbital_from_online(self, URL, meta_data={}, ID=None):
        orbital = self.model.load_data_from_online(URL, meta_data, ID=ID)
        self.add_orbital(orbital)

        return orbital.ID

    def get_orbitals(self):
        orbitals = [orbital[0] for orbital in self.model.orbitals]

        return orbitals

    def add_orbital(self, orbital):
        if "orientation" in orbital.meta_data:
            orientation = orbital.meta_data["orientation"]

        else:
            orientation = "xy"

        self.table.add_orbital(orbital, orientation)

        self.refresh_plot()

        self.orbital_added.emit(orbital.ID)

    def refresh_plot(self):
        data = self.model.update_displayed_plot_data()

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.plot_item.plot(data)
        self.crosshair.update_label()

    def refresh_mini_plots(self, ID, orbital_changed=True):
        parameters = self.get_parameters(ID)
        phi, theta, psi = parameters[3:6]
        E_kin = parameters[1]
        V0 = parameters[-1]

        if orbital_changed:
            orbital = self.model.ID_to_orbital(ID)
            self.mini_3Dkspace_plot.set_orbital(orbital, ID)
            self.mini_real_plot.set_orbital(orbital)

        self.mini_3Dkspace_plot.change_energy(E_kin)
        self.mini_3Dkspace_plot.change_inner_potential(V0)
        self.mini_3Dkspace_plot.rotate_orbital(phi, theta, psi)
        self.mini_real_plot.rotate_orbital(phi, theta, psi)

    def refresh_mini_plot_polarization(self):
        polarization, alpha, beta, _, s_share = self.polarization.get_parameters()[1:]

        self.mini_real_plot.rotate_photon(polarization, alpha, beta, s_share)

    def get_crosshair(self):
        return self.crosshair

    def get_parameters(self, ID):
        kinetic_energy, dk, symmetry, V0 = self.cube_options.get_parameters()
        parameters = self.table.get_parameters_by_ID(ID)
        weight, *orientation = parameters
        *polarization, s_share = self.polarization.get_parameters()

        return (
            weight,
            kinetic_energy,
            dk,
            *orientation,
            *polarization,
            symmetry,
            s_share,
            V0,
        )

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

    def export_to_numpy(self):
        path = config.get_key("paths", "numpy_export_start")
        if path == "None":
            file_name, _ = QFileDialog.getSaveFileName(None, "Save .npy File (*.npy)")
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, "Save .npy File (*.npy)", str(start_path)
            )

        if not file_name:
            return

        axis_1 = self.get_displayed_plot_data().x_axis
        axis_2 = self.get_displayed_plot_data().y_axis
        data = self.get_displayed_plot_data().data
        np.savez(file_name, axis_1=axis_1, axis_2=axis_2, data=data)

    def export_to_hdf5(self):
        if not self.interpolation.interpolation_checkbox.isChecked():
            print("Only interpolated OrbitalData can be exported.")
            return

        path = config.get_key("paths", "hdf5_export_start")
        if path == "None":
            file_name, _ = QFileDialog.getSaveFileName(None, "Save .hdf5 File (*.hdf5)")
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, "Save .hdf5 File (*.hdf5)", str(start_path)
            )

        if not file_name:
            return
        else:
            h5file = h5py.File(file_name, "w")

        export_energies = eval(config.get_key("orbital", "export_energies"))
        if isinstance(export_energies, dict):
            export_energies = np.linspace(
                export_energies["min"],
                export_energies["max"],
                export_energies["num"],
                endpoint=True,
            )

        kmaps = []
        old_energy = self.cube_options.energy_spinbox.value()
        for energy in export_energies:
            self.cube_options.energy_spinbox.setValue(energy)
            kmaps.append(self.get_displayed_plot_data().data)
        self.cube_options.energy_spinbox.setValue(old_energy)
        kmaps = np.array(kmaps)
        xrange, yrange = self.get_displayed_plot_data().range

        h5file.create_dataset("name", data="Orbitals")
        h5file.create_dataset("axis_1_label", data="E_kin")
        h5file.create_dataset("axis_2_label", data="kx")
        h5file.create_dataset("axis_3_label", data="ky")
        h5file.create_dataset("axis_1_units", data="eV")
        h5file.create_dataset("axis_2_units", data="1/Å")
        h5file.create_dataset("axis_3_units", data="1/Å")
        h5file.create_dataset(
            "axis_1_range", data=[export_energies[0], export_energies[-1]]
        )
        h5file.create_dataset("axis_2_range", data=xrange)
        h5file.create_dataset("axis_3_range", data=yrange)
        h5file.create_dataset(
            "data", data=kmaps, dtype="f8", compression="gzip", compression_opts=9
        )
        h5file.close()

    def export_to_txt(self):
        if not self.interpolation.interpolation_checkbox.isChecked():
            # Otherwise maps at different energies would be of different size
            print("Only interpolated OrbitalData can be exported.")
            return

        path = config.get_key("paths", "txt_export_start")
        if path == "None":
            file_name, _ = QFileDialog.getSaveFileName(None, "Save .itx File (*.itx)")
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, "Save .itx File (*.itx)", str(start_path)
            )

        if not file_name:
            return

        export_energies = eval(config.get_key("orbital", "export_energies"))
        if isinstance(export_energies, dict):
            export_energies = np.linspace(
                export_energies["min"],
                export_energies["max"],
                export_energies["num"],
                endpoint=True,
            )

        kmaps = []
        old_energy = self.cube_options.energy_spinbox.value()
        for energy in export_energies:
            self.cube_options.energy_spinbox.setValue(energy)
            kmaps.append(self.get_displayed_plot_data().data)
        self.cube_options.energy_spinbox.setValue(old_energy)
        kmaps = np.array(kmaps)
        xrange, yrange = self.get_displayed_plot_data().range
        shape = kmaps[0].shape
        xscale = (xrange[1] - xrange[0]) / shape[1]
        yscale = (yrange[1] - yrange[0]) / shape[0]
        name = Path(file_name).stem

        with open(file_name, "w") as f:
            f.write("IGOR\n")
            f.write(f"WAVES/N=({shape[1]},{shape[0]},{len(export_energies)})\t{name}\n")
            f.write("BEGIN\n")
            for data in kmaps:
                f.write("\t")
                np.savetxt(f, data.T, newline="\t")
            f.write("\nEND\n")
            f.write(f'X SetScale/P x {xrange[0]},{xscale}, "A^-1", {name}; ')
            f.write(f'SetScale/P y {yrange[0]},{yscale}, "A^-1", {name}; ')
            f.write(
                f'SetScale/P z {export_energies[0]},{export_energies[1]-export_energies[0]}, "eV", {name}; '
            )
            f.write(f'SetScale d 0,0, "", {name}\n')

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
        bottom = self.plot_item.get_label("bottom")
        left = self.plot_item.get_label("left")
        return bottom, left

    def save_state(self):
        orbital_save = []
        for orbital in self.model.orbitals:
            orbital_save.append(
                {
                    "ID": orbital[4],
                    "load_type": orbital[1],
                    "load_args": orbital[2],
                    "meta_data": orbital[3],
                }
            )

        save = {
            "orbitals": orbital_save,
            "title": self.title,
            "table": self.table.save_state(),
            "interpolation": self.interpolation.save_state(),
            "colormap": self.colormap.save_state(),
            "crosshair": self.crosshair.save_state(),
            "polarization": self.polarization.save_state(),
            "cube_options": self.cube_options.save_state(),
            "real_space_options": self.real_space_options.save_state(),
            "colorscale": self.plot_item.get_colormap(),
            "levels": self.plot_item.get_levels(),
        }

        return save, []

    def _setup(self):
        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap([self.plot_item])
        self.interpolation = Interpolation()

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(4, self.interpolation)
        layout.insertWidget(5, self.crosshair)

        self.mini_real_plot.set_options(self.real_space_options)
        self.mini_3Dkspace_plot.set_options(self.real_space_options)

        # Rough axis values for all orbitals to set labels for interpolation
        x = Axis("kx", "1/Å", [-3, 3], 200)
        y = Axis("ky", "1/Å", [-3, 3], 200)
        self.interpolation.set_label(x, y)
        self.plot_item.set_labels(x, y)

        self.title = "Orbitals"

    def _connect(self):
        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.table.orbital_changed.connect(self.orbitals_changed)
        self.table.orbital_removed.connect(self.remove_orbital_by_ID)
        self.table.orbital_selected.connect(self.refresh_mini_plots)
        self.polarization.polarization_changed.connect(self.change_parameter)
        self.polarization.polarization_changed.connect(
            self.refresh_mini_plot_polarization
        )
        self.cube_options.symmetrization_changed.connect(self.change_parameter)
        self.cube_options.energy_changed.connect(self.change_parameter)
        self.cube_options.V0_changed.connect(self.change_parameter)
        self.cube_options.resolution_changed.connect(self.change_parameter)
        self.cube_options.get_match_energy.connect(self.get_energy.emit)

        self.interpolation.smoothing_changed.connect(self.refresh_plot)
        self.interpolation.interpolation_changed.connect(self.refresh_plot)
