# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

# Third Party Imports
import numpy as np
import pyqtgraph as pg

# Own Imports
from kmap import __directory__
from kmap.config.config import config
from kmap.library.misc import normalize
from kmap.model.crosshair_model import CrosshairModel

# Load .ui File
UI_file = __directory__  / 'ui/crosshair.ui'
Crosshair_UI, _ = uic.loadUiType(UI_file)


class CrosshairBase(QWidget):
    crosshair_changed = pyqtSignal()

    def __init__(self, plot_item):

        super(CrosshairBase, self).__init__()

        self.plot_item = plot_item
        self._set_model()

        self.colors = ['k', 'w', 'r', 'b', 'g', 'c', 'm', 'y']

    def enable(self, enable):

        self.v_line.setVisible(enable)
        self.h_line.setVisible(enable)

    def update_label(self):

        plot_data = self.plot_item.get_plot_data()

        if plot_data == None:
            intensity = 0

        elif np.isnan(plot_data.data).all():
            intensity = np.nan

        else:
            cut = self.model.cut_from_data(plot_data, region='center')

            # Normalize by dividing by the number of non nan elements
            if config.get_key('crosshair', 'normalized_intensity') == 'True':
                intensity = normalize(cut.data)

            else:
                intensity = np.nansum(cut.data)

        if abs(intensity) > 1000:
            self.point_value_label.setText('%.2fk' % (intensity / 1000))

        else:
            self.point_value_label.setText('%.2f' % intensity)

        x = self.model.x
        y = self.model.y

        self.distance_value_label.setText('%.2f' % np.sqrt(x ** 2 + y ** 2))

    def move_crosshair_from_drag(self):

        x, y = self.v_line.value(), self.h_line.value()
        self.model.set_position(x, y)

        self.update()

    def move_crosshair_from_click(self, event):

        if not self.enable_crosshair_checkbox.isChecked():
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

    def change_color(self, index):

        self.h_line.setPen(self.colors[index])
        self.v_line.setPen(self.colors[index])

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

    def save_state(self):

        model_save = self.model.save_state()
        save = {'model': model_save,
                'enable_crosshair': self.enable_crosshair_checkbox.checkState(),
                'color': self.color_combobox.currentIndex()}

        return save

    def restore_state(self, save):

        self.model.restore_state(save['model'])
        self.update()
        self.update_label()
        self.move_crosshair_from_spinbox()
        self.enable_crosshair_checkbox.setCheckState(save['enable_crosshair'])
        self.color_combobox.setCurrentIndex(save['color'])

    def _set_model(self, model=None):

        if model is None:
            self.model = CrosshairModel(x=0, y=0)

        else:
            self.model = model

    def _setup(self):

        self.v_line = pg.InfiniteLine(movable=True, angle=90, pen='k',
                                      bounds=[self.x_spinbox.minimum(),
                                              self.x_spinbox.maximum()])
        self.h_line = pg.InfiniteLine(movable=True, angle=0, pen='k',
                                      bounds=[self.y_spinbox.minimum(),
                                              self.y_spinbox.maximum()])
        self.v_line.setValue(self.model.x)
        self.h_line.setValue(self.model.y)
        self.plot_item.addItem(self.v_line)
        self.plot_item.addItem(self.h_line)

    def _connect(self):

        self.x_spinbox.valueChanged.connect(self.move_crosshair_from_spinbox)
        self.y_spinbox.valueChanged.connect(self.move_crosshair_from_spinbox)

        self.enable_crosshair_checkbox.stateChanged.connect(self.enable)

        self.v_line.sigDragged.connect(self.move_crosshair_from_drag)
        self.h_line.sigDragged.connect(self.move_crosshair_from_drag)
        self.plot_item.view.scene().sigMouseClicked.connect(
            self.move_crosshair_from_click)

        self.color_combobox.currentIndexChanged.connect(self.change_color)


class Crosshair(CrosshairBase, Crosshair_UI):

    def __init__(self, plot_item):
        # Setup GUI
        super(Crosshair, self).__init__(plot_item)
        self.setupUi(self)

        self._setup()
        self._connect()

        self.enable(False)
        self.update_label()
