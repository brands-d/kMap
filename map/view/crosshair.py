from PyQt5.QtWidgets import QGroupBox
from map.ui.crosshair_ui import (
    CrosshairUI, CrosshairROIUI, CrosshairAnnulusUI)
from map.model.crosshair import Crosshair as CM
from map.model.crosshair import CrosshairWithROI as CRM
from map.model.crosshair import CrosshairWithAnnulus as CAM
import pyqtgraph as pg


class Crosshair(QGroupBox, CrosshairUI):

    def __init__(self, plot_item):

        super().__init__()

        self.plot_item = plot_item
        self._setup_plot_widgets()
        self._enable_crosshair(False)

        self.setupUi()

        self.set_crosshair_model()

    def _enable_crosshair(self, enable):

        self.v_line.setVisible(enable)
        self.h_line.setVisible(enable)

    def _setup_plot_widgets(self):

        self.v_line = pg.InfiniteLine(movable=True,
                                      angle=90,
                                      pen='k',
                                      bounds=[-10, 10])
        self.h_line = pg.InfiniteLine(movable=True,
                                      angle=0,
                                      pen='k',
                                      bounds=[-10, 10])

        self.plot_item.addItem(self.v_line)
        self.plot_item.addItem(self.h_line)

    def set_crosshair_model(self):

        self.crosshair = CM()

    def _move_crosshair_from_drag(self):

        self._update_spinboxes_silently(
            self.v_line.value(), self.h_line.value())
        self._move_crosshair_from_spinbox()

    def _move_crosshair_from_click(self, event):

        if not self.enable_crosshair.isChecked():
            return

        click_pos = self.plot_item.view.vb.mapSceneToView(
            event.scenePos())

        self._update_spinboxes_silently(click_pos.x(), click_pos.y())
        self._move_crosshair_from_spinbox()

    def _update_spinboxes_silently(self, x, y):

        self.x_spinbox.blockSignals(True)
        self.y_spinbox.blockSignals(True)

        self.x_spinbox.setValue(x)
        self.y_spinbox.setValue(y)

        self.x_spinbox.blockSignals(False)
        self.y_spinbox.blockSignals(False)

    def _move_crosshair_from_spinbox(self):

        self.v_line.setValue(self.x_spinbox.value())
        self.h_line.setValue(self.y_spinbox.value())


class CrosshairROI(Crosshair, CrosshairROIUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_roi = False
        self._enable_roi(False)

    def set_crosshair_model(self):

        self.crosshair = CRM()

    def _enable_roi(self, enable):

        self.roi.setVisible(enable)

    def _dragging_roi(self):

        self.dragging_roi = True

    def _setup_plot_widgets(self):

        super()._setup_plot_widgets()

        radius = 0.02
        pos = [self.v_line.value() - radius, self.h_line.value() - radius]
        self.roi = pg.CircleROI(pos,
                                size=[2 * radius, 2 * radius],
                                movable=False,
                                rotatable=False,
                                resizable=True,
                                removable=False,
                                pen='k',
                                handlePen='r')

        self.plot_item.addItem(self.roi)

    def _resize_roi_from_drag(self):

        if not self.dragging_roi:
            return

        self.dragging_roi = False

        self._update_roi_silently(self.roi.size()[0] / 2)
        self._resize_roi_from_spinbox()

    def _update_roi_silently(self, radius):

        self.roi_spinbox.blockSignals(True)

        self.roi_spinbox.setValue(radius)

        self.roi_spinbox.blockSignals(False)

    def _resize_roi_from_spinbox(self):

        radius = self.roi_spinbox.value()
        x = self.x_spinbox.value()
        y = self.y_spinbox.value()
        self.roi.setPos([x - radius, y - radius])
        self.roi.setSize([2 * radius, 2 * radius])

    def _move_crosshair_from_spinbox(self):

        super()._move_crosshair_from_spinbox()

        pos = [self.v_line.value() - self.roi_spinbox.value(),
               self.h_line.value() - self.roi_spinbox.value()]
        self.roi.setPos(pos)


class CrosshairAnnulus(CrosshairROI, CrosshairAnnulusUI):

    def __init__(self, plot_item):

        super().__init__(plot_item)

        self.dragging_an = False
        self._enable_an(False)

    def set_crosshair_model(self):

        self.crosshair = CAM()

    def _enable_an(self, enable):

        self.annulus.setVisible(enable)

    def _dragging_an(self):

        self.dragging_an = True

    def _setup_plot_widgets(self):

        super()._setup_plot_widgets()

        width = 0.1
        radius = self.roi.size()[0] + width
        pos = [self.v_line.value() - radius, self.h_line.value() - radius]
        self.annulus = pg.CircleROI(pos,
                                    size=[2 * radius, 2 * radius],
                                    movable=False,
                                    rotatable=False,
                                    resizable=True,
                                    removable=False,
                                    pen='k',
                                    handlePen='r')

        self.plot_item.addItem(self.annulus)

    def _resize_annulus_from_drag(self):

        if not self.dragging_an:
            return

        self.dragging_an = False

        self._update_annulus_silently(
            (self.annulus.size()[0] - self.roi.size()[0]) / 2)
        self._resize_annulus_from_spinbox()

    def _update_annulus_silently(self, width):

        self.an_spinbox.blockSignals(True)

        self.an_spinbox.setValue(width)

        self.an_spinbox.blockSignals(False)

    def _resize_annulus_from_spinbox(self):

        width = self.an_spinbox.value()
        radius = self.roi_spinbox.value() + width
        x = self.x_spinbox.value()
        y = self.y_spinbox.value()

        self.annulus.setPos([x - radius, y - radius])
        self.annulus.setSize([2 * radius, 2 * radius])

    def _move_crosshair_from_spinbox(self):

        super()._move_crosshair_from_spinbox()

        pos = [self.v_line.value() - self.roi_spinbox.value() -
               self.an_spinbox.value(),
               self.h_line.value() - self.roi_spinbox.value() -
               self.an_spinbox.value()]
        self.annulus.setPos(pos)

    def _resize_roi_from_spinbox(self):

        super()._resize_roi_from_spinbox()

        self._resize_annulus_from_spinbox()
