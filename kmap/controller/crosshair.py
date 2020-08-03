import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox
from kmap.ui.crosshair_ui import (
    CrosshairUI, CrosshairROIUI, CrosshairAnnulusUI)
from kmap.model.crosshair_model import (
    CrosshairModel, CrosshairWithROIModel, CrosshairWithAnnulusModel)
from kmap.config.config import config
from kmap.library.misc import normalize


class Crosshair(CrosshairUI):

    crosshair_changed = pyqtSignal()

    def __init__(self, plot_item):

        self.plot_item = plot_item
        self._set_model()

        CrosshairUI.__init__(self)

        self.enable(False)
        self.update_label()

    def enable(self, enable):

        self.v_line.setVisible(enable)
        self.h_line.setVisible(enable)

    def update_label(self):

        plot_data = self.plot_item.get_plot_data()

        if plot_data == None:
            intensity = 0

        else:
            cut = self.model.cut_from_data(plot_data, region='center')

            # Normalize by dividing by the number of non nan elements
            if config.get_key('crosshair', 'normalized_intensity') == 'True':
                intensity = normalize(cut)

            else:
                intensity = np.nansum(cut)

        if abs(intensity) > 1000:
            self.point_value.setText('%.2f  ka.u.' % (intensity / 1000))

        else:
            self.point_value.setText('%.2f  a.u.' % intensity)

        x = self.model.x
        y = self.model.y

        self.distance_value.setText('%.2f  Å^-1' % np.sqrt(x**2 + y**2))

    def move_crosshair_from_drag(self):

        x, y = self.v_line.value(), self.h_line.value()
        self.model.set_position(x, y)

        self.update()

    def move_crosshair_from_click(self, event):

        if not self.enable_crosshair.isChecked():
            return False

        click_pos = self.plot_item.view.vb.mapSceneToView(
            event.scenePos())
        self.model.set_position(click_pos.x(), click_pos.y())

        self.update()

        return True

    def move_crosshair_from_spinbox(self):

        x, y = self.x_spinbox.value(), self.y_spinbox.value()
        self.model.set_position(x, y)

        self.update()

    def update(self):

        x, y = self.model.x, self.model.y

        # Update Spinboxes silently
        self.x_spinbox.blockSignals(True)
        self.y_spinbox.blockSignals(True)
        self.x_spinbox.setValue(x)
        self.y_spinbox.setValue(y)
        self.x_spinbox.blockSignals(False)
        self.y_spinbox.blockSignals(False)

        # Update Crosshair Position
        self.v_line.setValue(x)
        self.h_line.setValue(y)

        # Emit Changed Signal
        self.crosshair_changed.emit()

    def _set_model(self):

        self.model = CrosshairModel(x=0, y=0)


class CrosshairROI(Crosshair, CrosshairROIUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_roi = False
        self.enable_roi(False)

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
                intensity = normalize(cut)

            else:
                intensity = np.nansum(cut)

        if abs(intensity) > 1000:
            self.area_value.setText('%.2f  ka.u.' % (intensity / 1000))

        else:
            self.area_value.setText('%.2f  a.u.' % intensity)

    def _set_model(self):

        self.model = CrosshairWithROI(x=0, y=0, radius=0.02)


class CrosshairAnnulus(CrosshairROI, CrosshairAnnulusUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_annulus = False
        self.enable_annulus(False)

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
                intensity = normalize(cut)

            else:
                intensity = np.nansum(cut)

        if abs(intensity) > 1000:
            self.ring_value.setText('%.2f  ka.u.' % (intensity / 1000))

        else:
            self.ring_value.setText('%.2f  a.u.' % intensity)

    def _set_model(self):

        self.model = CrosshairWithAnnulusModel(x=0, y=0, radius=0.2, width=0.1)
