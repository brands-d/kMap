# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic

# Own Imports
from kmap import __directory__
from kmap.library.misc import get_ID_from_tab_text
from kmap.library.qwidgetsub import Tab
from kmap.model.sliceddatatab_model import SlicedDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibWindow
from kmap.controller.dataslider import DataSlider
from kmap.controller.crosshairannulus import CrosshairAnnulus
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.colormap import Colormap


# Load .ui File
UI_file = __directory__ + '/ui/sliceddatatab.ui'
SlicedDataTab_UI, _ = uic.loadUiType(UI_file)


class SlicedDataTab(Tab, SlicedDataTab_UI):

    def __init__(self, path):

        self.model = SlicedDataTabModel(path)

        # Setup GUI
        super(SlicedDataTab, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.change_axis(0)
        self.change_slice(0)

    def get_title(self):

        data = self.model.data

        if data:
            id_ = data.ID

            if 'alias' in data.meta_data:
                text = data.meta_data['alias']
            else:
                text = data.name

            title = '%s (%i)' % (text, id_)

        else:
            title = 'NO DATA'

        return title

    def change_slice(self, index):

        axis = self.slider.get_axis()
        data = self.model.change_slice(index, axis)

        self.plot_item.plot(data)
        self.crosshair.update_label()

    def change_axis(self, axis):

        # 'axes' is a copy of all axes except the one with index 'axis'
        axes = [a for i, a in enumerate(self.model.data.axes) if i != axis]

        index = self.slider.get_index()
        data = self.model.change_slice(index, axis)

        self.plot_item.set_label(*axes)
        self.plot_item.plot(data)

    def crosshair_changed(self):

        self.crosshair.update_label()

    def display_in_matplotlib(self):

        data = self.model.displayed_plot_data
        LUT = self.plot_item.get_LUT()

        self.window = MatplotlibWindow(data, LUT=LUT)

    def closeEvent(self, event):

        del self.model

        Tab.closeEvent(self, event)

    def to_string(self):

        text = self.model.to_string()

        return text

    def _setup(self):

        self.slider = DataSlider(self.model.data)
        self.crosshair = CrosshairAnnulus(self.plot_item)
        self.colormap = Colormap(self.plot_item)

        layout = self.scroll_area.widget().layout()
        layout.insertWidget(0, self.slider)
        layout.insertWidget(1, self.colormap)
        layout.insertWidget(2, self.crosshair)

    def _connect(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.slice_changed.connect(self.change_slice)
        self.slider.axis_changed.connect(self.change_axis)
