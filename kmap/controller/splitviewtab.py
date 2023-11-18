import numpy as np
from PySide6.QtWidgets import QFileDialog

from kmap import __directory__
from kmap.config.config import config
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.dataslider import DataSliderNoTranspose
from kmap.controller.interpolation import Interpolation
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
from kmap.controller.splitviewoptions import SplitViewOptions
from kmap.library.qwidgetsub import Tab
from kmap.model.splitview_model import SplitViewTabModel
from kmap.ui.splitviewtab import Ui_splitviewtab as SplitViewTab_UI


class SplitViewTab(Tab, SplitViewTab_UI):
    def __init__(self, sliced_tab, orbital_tab):
        self.sliced_tab = sliced_tab
        self.orbital_tab = orbital_tab

        # Setup GUI
        super(SplitViewTab, self).__init__()
        self.setupUi(self)

        self._setup()
        self._connect()

        self.change_axis(0)
        self.change_slice(0)

    @classmethod
    def init_from_save(cls, save, dependencies, tab_widget):
        sliced_tab = tab_widget.get_tab_by_ID(dependencies["sliced_tab"])
        orbital_tab = tab_widget.get_tab_by_ID(dependencies["orbital_tab"])
        tab = SplitViewTab(sliced_tab, orbital_tab)
        tab.locked_tabs = [sliced_tab, orbital_tab]

        tab.slider.restore_state(save["slider"]),
        tab.crosshair.restore_state(save["crosshair"]),
        tab.interpolation.restore_state(save["interpolation"]),
        tab.split_options.restore_state(save["split_options"])
        tab.colormap.restore_state(save["colormap"])
        tab.plot_item.set_colormap(save["colorscale"])
        tab.plot_item.set_levels(save["levels"])

        return tab

    def save_state(self):
        save = {
            "title": self.title,
            "slider": self.slider.save_state(),
            "crosshair": self.crosshair.save_state(),
            "colorscale": self.plot_item.get_colormap(),
            "levels": self.plot_item.get_levels(),
            "interpolation": self.interpolation.save_state(),
            "split_options": self.split_options.save_state(),
            "colormap": self.colormap.save_state(),
        }

        dependencies = {
            "sliced_tab": self.sliced_tab.ID,
            "orbital_tab": self.orbital_tab.ID,
        }

        return save, dependencies

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

        index = self.get_slice()
        axis = self.slider.get_axis()
        data = self.model.update_displayed_plot_data(index, axis)
        axis_1 = data.x_axis
        axis_2 = data.y_axis
        np.savez(file_name, axis_1=axis_1, axis_2=axis_2, data=data.data)

    def get_title(self):
        return self.title

    def get_axis(self):
        return self.slider.get_axis()

    def get_slice(self):
        return self.slider.get_index()

    def change_slice(self, index=-1):
        axis = self.slider.get_axis()
        slice_index = index if index != -1 else self.get_slice()
        data = self.model.update_displayed_plot_data(slice_index, axis)

        self.plot_item.plot(data)
        self.crosshair.update_label()

    def change_axis(self, axis):
        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.get_sliced_data().axes) if i != axis]
        index = self.get_slice()
        data = self.model.update_displayed_plot_data(index, axis)

        self.plot_item.set_labels(axes[1], axes[0])
        self.interpolation.set_label(axes[1], axes[0])
        self.plot_item.plot(data)

    def crosshair_changed(self):
        self.crosshair.update_label()

    def display_in_matplotlib(self):
        data = self.model.displayed_plot_data
        LUT = self.plot_item.get_LUT()

        window = MatplotlibImageWindow(data, LUT=LUT)

        return window

    def change_split_options(self, scale, type_):
        self.model.set_scale(scale)
        self.model.set_type(type_)
        self.change_slice()

    def change_symmetry(self, symmetry, mirror):
        self.model.change_symmetry(symmetry, mirror)
        self.change_axis(self.slider.get_axis())

    def closeEvent(self, event):
        del self.model

        Tab.closeEvent(self, event)

    def _setup(self):
        self.title = "Split View"
        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap(self.plot_item)
        self.interpolation = Interpolation()
        self.interpolation.set_force_interpolation(True)
        self.model = SplitViewTabModel(
            self.sliced_tab, self.orbital_tab, self.interpolation
        )
        self.split_options = SplitViewOptions()

        self.slider = DataSliderNoTranspose(self.model.get_sliced_data())

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.split_options)
        layout.insertWidget(2, self.interpolation)
        layout.insertWidget(3, self.colormap)
        layout.insertWidget(4, self.crosshair)

    def _connect(self):
        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
        self.slider.symmetry_changed.connect(self.change_symmetry)
        self.interpolation.smoothing_changed.connect(self.change_slice)
        self.interpolation.interpolation_changed.connect(self.change_slice)
        self.split_options.values_changed.connect(self.change_split_options)
