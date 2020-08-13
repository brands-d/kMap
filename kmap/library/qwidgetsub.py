# Python Imports
from abc import abstractmethod

# PyQt5 Imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QCheckBox, QDoubleSpinBox, QWidget


class CenteredLabel(QLabel):

    def __init__(self, *args, **kwargs):

        super(CenteredLabel, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)


class UseCheckBox(QCheckBox):

    def __init__(self, *args, **kwargs):

        super(UseCheckBox, self).__init__(*args, **kwargs)

        self.setChecked(True)


class AngleSpinBox(QDoubleSpinBox):

    def __init__(self, value, objectname, *args, **kwargs):

        super(AngleSpinBox, self).__init__(*args, **kwargs)

        self.setSuffix('°')
        self.setValue(value)
        self.setMinimum(-90)
        self.setMaximum(90)
        self.setDecimals(1)
        self.setSingleStep(1)
        self.setKeyboardTracking(False)
        self.setAlignment(Qt.AlignHCenter)
        self.setObjectName(objectname)


class WeightSpinBox(QDoubleSpinBox):

    def __init__(self, *args, **kwargs):

        super(WeightSpinBox, self).__init__(*args, **kwargs)

        self.setValue(1)
        self.setMinimum(-99999.9)
        self.setMaximum(99999.9)
        self.setDecimals(1)
        self.setSingleStep(0.1)
        self.setKeyboardTracking(False)
        self.setAlignment(Qt.AlignHCenter)
        self.setObjectName('weight')


class AspectWidget(QWidget):

    def __init__(self, *args, ratio=0, **kwargs):

        self.ratio = ratio

        super().__init__(*args, **kwargs)

    def set_ratio(self, ratio):

        self.ratio = ratio

    def heightForWidth(self, width):

        return int(width / self.ratio)

    def widthForHeight(self, height):

        return int(height * self.ratio)

    def resizeEvent(self, event):
        '''BUG: For unknown reasons the resizeEvent is called multiple
        times with outdated sizes, thus if the user lowers the side that
        is too large, it will not update correctly.'''
        event.ignore()

        if self.ratio == 0:
            return

        old_width = event.oldSize().width()
        old_height = event.oldSize().height()
        new_width = event.size().width()
        new_height = event.size().height()

        if old_width == new_width:
            if old_height == new_height:
                # No change
                return

            else:
                # Only height changed -> use height
                height = new_height
                width = self.widthForHeight(height)

        else:
            if old_height == new_height:
                # Only width changed -> use width
                width = new_width
                height = self.heightForWidth(width)

            else:
                # Both changed -> use larger one
                if new_width >= new_height:
                    # Width is larger
                    width = new_width
                    height = self.heightForWidth(width)

                else:
                    # Height is larger
                    height = new_height
                    width = self.widthForHeight(height)

        self.blockSignals(True)
        self.resize(width, height)
        self.blockSignals(False)


class Tab(QWidget):

    def __init__(self, *args, **kwargs):

        super(Tab, self).__init__(*args, **kwargs)

    @abstractmethod
    def get_title(self):
        pass

    def closeEvent(self, event):

        self.deleteLater()
        event.accept()
