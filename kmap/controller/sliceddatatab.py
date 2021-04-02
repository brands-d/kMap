# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.model.sliceddatatab_model import SlicedDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibImageWindow
from kmap.controller.interpolation import Interpolation
from kmap.controller.dataslider import DataSlider
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.colormap import Colormap

# Load .ui File
UI_file = __directory__ / 'ui/sliceddatatab.ui'
SlicedDataTab_UI, _ = uic.loadUiType(UI_file)


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
    def init_from_save(cls, save):
        load_type = save['model']['load_type']
        load_args = save['model']['load_args']

        if load_type == 'load_from_path':
            tab = SlicedDataTab.init_from_path(load_args)

        elif load_type == 'load_from_cube':
            tab = SlicedDataTab.init_from_cube(load_args)

        elif load_type == 'load_from_URL':
            tab = SlicedDataTab.init_from_URL(load_args)

        elif load_type == 'load_from_URLs':
            tab = SlicedDataTab.init_from_URLs(load_args)

        else:
            raise ValueError

        tab.slider.restore_state(save['slider'])
        tab.crosshair.restore_state(save['crosshair'])
        tab.interpolation.restore_state(save['interpolation'])
        tab.colormap.restore_state(save['colormap'])

        new_ID = tab.model.data.ID
        return tab, [[save['model']['ID'], new_ID]]

    def save_state(self):
        save = {'title': self.title,
                'model': self.model.save_state(),
                'slider': self.slider.save_state(),
                'crosshair': self.crosshair.save_state(),
                'interpolation': self.interpolation.save_state(),
                'colormap': self.colormap.save_state()}

        return save, []

    def get_data(self):
        return self.model.data

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
        bottom = self.plot_item.get_label('bottom')
        left = self.plot_item.get_label('left')
        return bottom, left

    def transpose(self, constant_axis):
        self.model.transpose(constant_axis)
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

            if 'alias' in data.meta_data:
                text = data.meta_data['alias']
            else:
                text = data.name

            self.title = '%s (%i)' % (text, id_)

        else:
            self.title = 'NO DATA'

    def _connect(self):
        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
        self.slider.tranpose_triggered.connect(self.transpose)
        self.slider.symmetry_changed.connect(self.change_symmetry)
        self.interpolation.smoothing_changed.connect(self.change_slice)
        self.interpolation.interpolation_changed.connect(self.change_slice)
