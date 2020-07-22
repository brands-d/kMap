from PyQt5.QtWidgets import QGroupBox
from map.ui.crosshair_ui import (
    CrosshairUI, CrosshairROIUI, CrosshairAnnulusUI)
from map.model.crosshair import Crosshair as CrosshairModel
from map.model.crosshair import (
    CrosshairWithAnnulus as CrosshairWithAnnulusModel)
import numpy as np
from PyQt5.QtCore import pyqtSignal


class Crosshair(QGroupBox, CrosshairUI):

    crosshair_changed = pyqtSignal()

    def __init__(self, plot_item):

        super().__init__()

        self._set_crosshair_model()
        self.plot_item = plot_item

        self.setupUi()

        self.enable(False)
        self.update_label(None)

    def _set_crosshair_model(self):

        self.model = CrosshairModel(x=0, y=0)

    def enable(self, enable):

        self.v_line.setVisible(enable)
        self.h_line.setVisible(enable)

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

    def update_label(self, plot_data):

        if plot_data == None:
            self.point_value.setText('0.00  a.u.')

        else:
            intensity = np.nansum(
                self.model.cut_from_data(plot_data, region='center'))

            self.point_value.setText('%.2f  a.u.' % intensity)


class CrosshairROI(Crosshair, CrosshairROIUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_roi = False
        self.enable_roi(False)

    def _set_crosshair_model(self):

        self.model = CrosshairWithROI(x=0, y=0, radius=0.02)

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

    def update_label(self, plot_data):

        super().update_label(plot_data)

        if plot_data == None:
            self.area_value.setText('0.00  a.u.')

        else:
            intensity = np.nansum(
                self.model.cut_from_data(plot_data, region='roi'))

            self.area_value.setText('%.2f  a.u.' % intensity)


class CrosshairAnnulus(CrosshairROI, CrosshairAnnulusUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_annulus = False
        self.enable_annulus(False)

    def _set_crosshair_model(self):

        self.model = CrosshairWithAnnulusModel(x=0, y=0, radius=0.2, width=0.1)

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

    def update_label(self, plot_data):

        super().update_label(plot_data)

        if plot_data == None:
            self.ring_value.setText('0.00  a.u.')

        else:
            intensity = np.nansum(
                self.model.cut_from_data(plot_data, region='ring'))

            self.ring_value.setText('%.2f  a.u.' % intensity)
