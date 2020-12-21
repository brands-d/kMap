# Python Imports
import numpy as np
import pyqtgraph as pg

# PyQt5 Imports
from PyQt5 import uic

# Own Imports
from kmap import __directory__
from kmap.config.config import config
from kmap.library.misc import normalize
from kmap.model.crosshair_model import CrosshairROIModel
from kmap.controller.crosshair import CrosshairBase

# Load .ui File
UI_file = __directory__ / 'ui/crosshairroi.ui'
CrosshairROI_UI, _ = uic.loadUiType(UI_file)


class CrosshairROIBase(CrosshairBase):

    def __init__(self, plot_item):

        super().__init__(plot_item)

    def enable_roi(self, enable):

        self.roi.setVisible(enable)

    def dragging_roi(self):

        self.dragging_roi = True

    def resize_roi_from_drag(self):

        # There is no signal for finished dragging, but starting it
        if not self.dragging_roi:
            return

        self.dragging_roi = False

        radius = self.roi.size()[0] / 2

        if radius <= 0:
            radius = 0.01

        self.model.set_radius(radius)

        self.update()

    def resize_roi_from_spinbox(self):

        radius = self.roi_spinbox.value()

        if radius <= 0:
            radius = 0.01

        self.model.set_radius(radius)

        self.update()

    def move_crosshair_from_spinbox(self):

        update = super().move_crosshair_from_spinbox()

        if update:
            x, y = self.model.x, self.model.y
            self.roi.setPos(x, y)

            return True

        else:
            return False

    def change_color(self, index):

        CrosshairBase.change_color(self, index)

        self.roi.setPen(self.colors[index])

    def update(self):

        x, y, radius = self.model.x, self.model.y, self.model.radius

        # Update Spinboxes silently
        self.roi_spinbox.blockSignals(True)
        self.roi_spinbox.setValue(radius)
        self.roi_spinbox.blockSignals(False)

        # Update Crosshair Position and Size
        self.roi.setPos([x - radius, y - radius])
        self.roi.setSize([2 * radius, 2 * radius])

        super().update()

    def update_label(self):

        super().update_label()

        plot_data = self.plot_item.get_plot_data()

        if plot_data == None:
            intensity = 0

        else:
            cut = self.model.cut_from_data(plot_data, region='roi')

            # Normalize by dividing by the number of non nan elements
            if config.get_key('crosshair', 'normalized_intensity') == 'True':
                intensity = normalize(cut.data)

            else:
                intensity = np.nansum(cut.data)

        if abs(intensity) > 1000:
            self.area_value_label.setText('%.2fk' % (intensity / 1000))

        else:
            self.area_value_label.setText('%.2f' % intensity)

    def save_state(self):

        save = super().save_state()
        save.update(
            {'enable_roi': self.enable_roi_checkbox.checkState()})

        return save

    def restore_state(self, save):

        super().restore_state(save)

        self.enable_roi_checkbox.setCheckState(save['enable_roi'])

    def _set_model(self, model=None):

        if model is None:
            self.model = CrosshairROIModel(x=0, y=0, radius=0.2)

        else:
            self.model = model

    def _setup(self):

        CrosshairBase._setup(self)

        x, y, radius = self.model.x, self.model.y, self.model.radius

        self.roi = pg.CircleROI([x - radius, y - radius],
                                size=[2 * radius, 2 * radius],
                                movable=False,
                                rotatable=False,
                                resizable=True,
                                removable=False,
                                pen='k')
        self.plot_item.addItem(self.roi)

    def _connect(self):

        CrosshairBase._connect(self)

        self.enable_roi_checkbox.stateChanged.connect(self.enable_roi)

        self.roi_spinbox.valueChanged.connect(self.resize_roi_from_spinbox)
        self.roi.sigRegionChangeFinished.connect(self.resize_roi_from_drag)
        self.roi.sigRegionChangeStarted.connect(self.dragging_roi)


class CrosshairROI(CrosshairROIBase, CrosshairROI_UI):

    def __init__(self, plot_item):
        # Setup GUI
        super(CrosshairROI, self).__init__(plot_item)
        self.setupUi(self)
        self._setup()
        self._connect()

        self.dragging_roi = False
        self.enable_roi(False)

        self.enable(False)
        self.update_label()
