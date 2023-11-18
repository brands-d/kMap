from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.ui.splitviewoptions import Ui_cubeoptions as SplitViewOptions_UI


class SplitViewOptions(QWidget, SplitViewOptions_UI):
    values_changed = Signal(float, str)

    def __init__(self, *args, **kwargs):
        # Setup GUI
        super(SplitViewOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def save_state(self):
        scale = self.scale_spinbox.value()
        type_ = self.type_combobox.currentIndex()

        save = {"Scale": scale, "Type": type_}

        return save

    def restore_state(self, save):
        scale = save["Scale"]
        type_ = save["Type"]

        self.scale_spinbox.setValue(scale)
        self.type_combobox.setCurrentIndex(type_)

    def get_parameters(self):
        scale = self.scale_spinbox.value()
        type_ = self.type_combobox.currentText()

        return scale, type_

    def emit_values(self):
        scale, type_ = self.get_parameters()
        self.values_changed.emit(scale, type_)

    def _connect(self):
        self.scale_spinbox.valueChanged.connect(self.emit_values)
        self.type_combobox.currentIndexChanged.connect(self.emit_values)
