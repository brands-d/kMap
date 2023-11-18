from pathlib import Path

import numpy as np
from PySide6.QtWidgets import QFileDialog

from kmap import __directory__
from kmap.config.config import config
from kmap.controller.colormap import Colormap
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.dataslider import DataSlider
from kmap.controller.interpolation import Interpolation
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
from kmap.library.qwidgetsub import Tab
from kmap.model.sliceddatatab_model import SlicedDataTabModel
from kmap.ui.sliceddatatab import Ui_sliceddatatab as SlicedDataTab_UI


class SlicedDataTab(Tab, SlicedDataTab_UI):
    def __init__(self, model):
        self.model = model
        # Setup GUI
        super(SlicedDataTab, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.change_axis(0)
        self.change_slice(0)

    @classmethod
    def init_from_URLs(cls, URLs):
        model = SlicedDataTabModel()
        model.load_data_from_URLs(URLs)

        return cls(model)

    @classmethod
    def init_from_URL(cls, URL):
        model = SlicedDataTabModel()
        model.load_data_from_URL(URL)

        return cls(model)

    @classmethod
    def init_from_cube(cls, URL):
        model = SlicedDataTabModel()
        model.load_data_from_cube(URL)

        return cls(model)

    @classmethod
    def init_from_path(cls, path):
        model = SlicedDataTabModel()
        model.load_data_from_path(path)

        return cls(model)

    @classmethod
    def init_from_save(cls, save, dependencies, tab_widget=None):
        model = SlicedDataTabModel()
        model.restore_state(save["model"])
        self = cls(model)

        self.slider.restore_state(save["slider"])
        self.interpolation.restore_state(save["interpolation"])
        self.crosshair.restore_state(save["crosshair"])
        self.colormap.restore_state(save["colormap"])
        self.plot_item.set_levels(save["levels"])
        self.plot_item.set_colormap(save["colorscale"])

        return self

    def save_state(self):
        save = {
            "title": self.title,
            "colorscale": self.plot_item.get_colormap(),
            "levels": self.plot_item.get_levels(),
            "model": self.model.save_state(),
            "slider": self.slider.save_state(),
            "crosshair": self.crosshair.save_state(),
            "interpolation": self.interpolation.save_state(),
            "colormap": self.colormap.save_state(),
        }

        return save, []

    def get_data(self):
        return self.model.data

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

        old_index = self.get_slice()
        axis_1 = self.model.data.axes[0].axis
        axis_2 = self.get_displayed_plot_data().x_axis
        axis_3 = self.get_displayed_plot_data().y_axis
        data = np.zeros(
            (
                self.model.data.axes[self.get_axis()].num,
                *self.get_displayed_plot_data().data.shape,
            )
        )
        for i in list(range((int(self.model.data.axes[self.get_axis()].num)))):
            self.change_slice(i)
            data[i, :, :] = self.get_displayed_plot_data().data
        np.savez(file_name, axis_1=axis_1, axis_2=axis_2, axis_3=axis_3, slices=data)
        self.change_slice(old_index)

    def export_to_txt(self):
        path = config.get_key("paths", "txt_export_start")
        if path == "None":
            file_name, _ = QFileDialog.getSaveFileName(None, "Save .txt File (*.txt)")
        else:
            start_path = str(__directory__ / path)
            file_name, _ = QFileDialog.getSaveFileName(
                None, "Save .txt File (*.txt)", str(start_path)
            )

        if not file_name:
            return

        old_index = self.get_slice()
        z = self.model.data.axes[self.get_axis()]
        y, x = [a for i, a in enumerate(self.model.data.axes) if i != self.get_axis()]
        shape = self.get_displayed_plot_data().data.shape
        xrange, yrange = self.get_displayed_plot_data().range
        xscale = (xrange[1] - xrange[0]) / shape[1]
        yscale = (yrange[1] - yrange[0]) / shape[0]
        indicies = list(range((int(z.num))))
        name = Path(file_name).stem

        with open(file_name, "w") as f:
            f.write("IGOR\n")
            f.write(f"WAVES/N=({shape[1]},{shape[0]},{len(indicies)})\t{name}\n")
            f.write("BEGIN\n")
            for i in indicies:
                f.write("\t")
                self.change_slice(i)
                np.savetxt(
                    f, self.get_displayed_plot_data().data.T.flatten(), newline="\t"
                )

            f.write("\nEND\n")
            f.write(f'X SetScale/P x {xrange[0]},{xscale}, "{x.units}", {name}; ')
            f.write(f'SetScale/P y {yrange[0]},{yscale}, "{y.units}", {name}; ')
            f.write(f'SetScale/P z {z.range[0]},{z.stepsize}, "{z.units}", {name}; ')
            f.write(f'SetScale d 0,0, "", {name}\n')

        self.change_slice(old_index)

    def get_axis(self):
        return self.slider.get_axis()

    def get_slice(self):
        return self.slider.get_index()

    def change_slice(self, index=-1):
        axis = self.slider.get_axis()
        slice_index = index if index != -1 else self.get_slice()
        data = self.model.change_slice(slice_index, axis)

        data = self.interpolation.interpolate(data)
        data = self.interpolation.smooth(data)

        self.plot_item.plot(data)
        self.crosshair.update_label()

    def change_axis(self, axis):
        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.data.axes) if i != axis]

        index = self.get_slice()
        data = self.model.change_slice(index, axis)

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

    def closeEvent(self, event):
        del self.model

        Tab.closeEvent(self, event)

    def to_string(self):
        text = self.model.to_string()

        return text

    def get_displayed_plot_data(self):
        return self.model.displayed_plot_data

    def get_crosshair(self):
        return self.crosshair

    def get_plot_labels(self):
        bottom = self.plot_item.get_label("bottom")
        left = self.plot_item.get_label("left")
        return bottom, left

    def transpose(self, axis_order):
        self.model.transpose(axis_order)
        self.change_axis(self.slider.get_axis())

    def change_symmetry(self, symmetry, mirror):
        self.model.change_symmetry(symmetry, mirror)
        self.change_axis(self.slider.get_axis())

    def _setup(self):
        self.slider = DataSlider(self.model.data)
        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap(self.plot_item)
        self.interpolation = Interpolation()

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)
        layout.insertWidget(3, self.interpolation)

        # Set Title
        data = self.model.data

        if data:
            id_ = data.ID

            if "alias" in data.meta_data:
                text = data.meta_data["alias"]
            else:
                text = data.name

            self.title = "%s (%i)" % (text, id_)

        else:
            self.title = "NO DATA"

    def _connect(self):
        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
        self.slider.tranpose_triggered.connect(self.transpose)
        self.slider.symmetry_changed.connect(self.change_symmetry)
        self.interpolation.smoothing_changed.connect(self.change_slice)
        self.interpolation.interpolation_changed.connect(self.change_slice)
