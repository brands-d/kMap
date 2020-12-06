# Python Imports
import numpy as np
import pyqtgraph as pg

# PyQt5 Imports
from PyQt5 import uic

# Own Imports
from kmap import __directory__
from kmap.config.config import config
from kmap.library.misc import normalize
from kmap.model.crosshair_model import CrosshairAnnulusModel
from kmap.controller.crosshairroi import CrosshairROIBase

# Load .ui File
UI_file = __directory__ / 'ui/crosshairannulus.ui'
CrosshairAnnulus_UI, _ = uic.loadUiType(UI_file)


class CrosshairAnnulusBase(CrosshairROIBase):

    def __init__(self, plot_item):

        super().__init__(plot_item)

    def enable_annulus(self, enable):

        self.annulus.setVisible(enable)

    def dragging_annulus(self):

        self.dragging_annulus = True

    def resize_annulus_from_drag(self):

        # There is no signal for finished dragging, but starting it
        if not self.dragging_annulus:
            return

        self.dragging_annulus = False

        width = (self.annulus.size()[0] - self.roi.size()[0]) / 2

        if width <= 0:
            width = 0.01

        self.model.set_width(width)

        self.update()

    def resize_annulus_from_spinbox(self):

        width = self.width_spinbox.value()

        if width <= 0:
            width = 0.01

        self.model.set_width(width)

        self.update()

    def move_crosshair_from_spinbox(self):

        update = super().move_crosshair_from_spinbox()

        if update:
            x, y = self.model.x, self.model.y
            self.annulus.setPos(x, y)

            return True

        else:
            return False

    def change_color(self, index):

        CrosshairROIBase.change_color(self, index)

        self.annulus.setPen(self.colors[index])

    def update(self):

        x, y = self.model.x, self.model.y
        radius, width = self.model.radius, self.model.width
        large_radius = radius + width
        # Update Spinboxes silently
        self.roi_spinbox.blockSignals(True)
        self.width_spinbox.setValue(width)
        self.roi_spinbox.blockSignals(False)

        # Update Crosshair Position and Size
        self.annulus.setPos([x - large_radius, y - large_radius])
        self.annulus.setSize([2 * large_radius, 2 * large_radius])

        super().update()

    def update_label(self):

        plot_data = self.plot_item.get_plot_data()

        super().update_label()

        if plot_data == None:
            intensity = 0

        else:
            cut = self.model.cut_from_data(plot_data, region='ring')

            # Normalize by dividing by the number of non nan elements
            if config.get_key('crosshair', 'normalized_intensity') == 'True':
                intensity = normalize(cut.data)

            else:
                intensity = np.nansum(cut.data)

        if abs(intensity) > 1000:
            self.ring_value_label.setText('%.2fk' % (intensity / 1000))

        else:
            self.ring_value_label.setText('%.2f' % intensity)

    def save_state(self):

        save = super().save_state()
        save.update(
            {'enable_annulus': self.enable_annulus_checkbox.checkState()})

        return save

    def restore_state(self, save):

        super().restore_state(save)

        self.enable_annulus_checkbox.setCheckState(save['enable_annulus'])

    def _set_model(self, model=None):

        if model is None:
            self.model = CrosshairAnnulusModel(x=0, y=0, radius=0.2, width=0.1)

        else:
            self.model = model

    def _setup(self):

        CrosshairROIBase._setup(self)

        x, y = self.model.x, self.model.y
        radius, width = self.model.radius, self.model.width
        large_radius = radius + width
        self.annulus = pg.CircleROI([x - large_radius, y - large_radius],
                                    size=[2 * large_radius, 2 * large_radius],
                                    movable=False,
                                    rotatable=False,
                                    resizable=True,
                                    removable=False,
                                    pen='k')
        self.plot_item.addItem(self.annulus)

    def _connect(self):

        CrosshairROIBase._connect(self)

        self.enable_annulus_checkbox.stateChanged.connect(self.enable_annulus)

        self.width_spinbox.valueChanged.connect(
            self.resize_annulus_from_spinbox)
        self.annulus.sigRegionChangeFinished.connect(
            self.resize_annulus_from_drag)
        self.annulus.sigRegionChangeStarted.connect(self.dragging_annulus)


class CrosshairAnnulus(CrosshairAnnulusBase, CrosshairAnnulus_UI):

    def __init__(self, plot_item):
        # Setup GUI
        super(CrosshairAnnulus, self).__init__(plot_item)
        self.setupUi(self)
        self._setup()
        self._connect()

        self.dragging_roi = False
        self.enable_roi(False)
        self.dragging_annulus = False
        self.enable_annulus(False)

        self.enable(False)
        self.update_label()
