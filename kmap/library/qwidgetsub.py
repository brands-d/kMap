# PyQt5 Imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QCheckBox, QDoubleSpinBox


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
        self.setObjectName('weight')
