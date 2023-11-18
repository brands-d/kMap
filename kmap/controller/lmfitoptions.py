import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap import __directory__
from kmap.config.config import config
from kmap.ui.lmfitoptions import Ui_lmfit as LMFitOptions_UI


class LMFitOptions(QWidget, LMFitOptions_UI):
    fit_triggered = Signal()
    region_changed = Signal(str, bool)
    background_changed = Signal(str)
    method_changed = Signal(str)
    slice_policy_changed = Signal(str)

    def __init__(self, parent):
        # Setup GUI
        super(LMFitOptions, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect(parent)

    def save_state(self):
        save = {
            "slices": self.slice_combobox.currentIndex(),
            "region": self.region_comboBox.currentIndex(),
            "slice_range": (
                self.from_slice_spinbox.value(),
                self.to_slice_spinbox.value(),
            ),
            "method": self.method_combobox.currentIndex(),
            "background": self.background_combobox.currentText(),
        }

        return save

    def restore_state(self, save):
        self.slice_combobox.setCurrentIndex(save["slices"])
        self.region_comboBox.setCurrentIndex(save["region"])
        self.method_combobox.setCurrentIndex(save["method"])
        self.background_combobox.setCurrentText(save["background"])
        self.from_slice_spinbox.setValue(save["slice_range"][0])
        self.to_slice_spinbox.setValue(save["slice_range"][1])

    def get_region(self):
        text = self.region_comboBox.currentText()

        if text == "Entire kMap":
            region = "all"
            inverted = False

        elif text == "Only ROI":
            region = "roi"
            inverted = False

        elif text == "Only Annulus":
            region = "ring"
            inverted = False

        elif text == "Except ROI":
            region = "roi"
            inverted = True

        elif text == "Except Annulus":
            region = "ring"
            inverted = True

        return region, inverted

    def get_method(self):
        text = self.method_combobox.currentText()

        return text[text.find("(") + 1 : text.find(")")]

    def get_slice_policy(self):
        index = self.slice_combobox.currentIndex()

        if index == 0:
            self.from_slice_spinbox.setEnabled(False)
            self.to_slice_spinbox.setEnabled(False)

            return "only one"

        elif index == 1:
            self.from_slice_spinbox.setEnabled(False)
            self.to_slice_spinbox.setEnabled(False)

            return "all"

        elif index == 2:
            self.from_slice_spinbox.setEnabled(False)
            self.to_slice_spinbox.setEnabled(False)

            return "all combined"

        else:
            self.from_slice_spinbox.setEnabled(True)
            self.to_slice_spinbox.setEnabled(True)

            from_ = self.from_slice_spinbox.value()
            to_ = self.to_slice_spinbox.value()
            indices = range(from_, to_ + 1)

            if not indices:
                indices = [from_]

            return " ".join(str(e) for e in indices)

    def get_background(self):
        return self.background_combobox.currentText()

    def update_fit_button(self):
        self.fit_button.setText("Fit")
        self.fit_button.repaint()

    def _trigger_fit(self):
        self.fit_button.setText("Running")
        self.fit_button.repaint()

        self.fit_triggered.emit()

    def _change_region(self):
        region, inverted = self.get_region()

        self.region_changed.emit(region, inverted)

    def _change_method(self):
        method = self.get_method()

        self.method_changed.emit(method)

    def _change_slice_policy(self):
        slice_policy = self.get_slice_policy()
        self.slice_policy_changed.emit(slice_policy)

    def _pre_factor_background(self):
        background = "c*" + self.get_background()
        self.background_combobox.setCurrentText(background)

    def _change_background(self):
        equation = self.get_background()
        self.background_changed.emit(equation)

    def _setup(self):
        temp = __directory__ / config.get_key("paths", "equations")
        default = temp / "background_equations_default"
        user = temp / "background_equations_user"
        self.path = user if os.path.isfile(user) else default

        with open(self.path, "r") as file:
            equations = file.read().split("\n")

        for equation in equations:
            self.background_combobox.addItem(equation)

        self.background_combobox.setCurrentIndex(0)

    def _connect(self, parent):
        parent.fit_finished.connect(self.update_fit_button)
        self.fit_button.clicked.connect(self._trigger_fit)
        self.region_comboBox.currentIndexChanged.connect(self._change_region)
        self.method_combobox.currentIndexChanged.connect(self._change_method)
        self.slice_combobox.currentIndexChanged.connect(self._change_slice_policy)
        self.background_combobox.currentIndexChanged.connect(self._change_background)
        self.background_combobox.currentTextChanged.connect(self._change_background)
        self.from_slice_spinbox.valueChanged.connect(self._change_slice_policy)
        self.to_slice_spinbox.valueChanged.connect(self._change_slice_policy)
