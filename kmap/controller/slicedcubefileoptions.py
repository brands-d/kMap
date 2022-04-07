# PyQt5 Imports
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ / 'ui/slicedcubefileoptions.ui'
SlicedDataBaseOptions_UI, _ = uic.loadUiType(UI_file)


class SlicedCubefileOptions(QWidget, SlicedDataBaseOptions_UI):

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(SlicedCubefileOptions, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()

    def get_parameters(self):

        name = self.line_edit.text()
        name = name if name else 'no name given'
        E_kin_max = self.Ekin_max_spinbox.value()
        dk3D = self.dk3D_step_spinbox.value()
        domain_index = self.domain_combobox.currentIndex()
        value_index = self.value_combobox.currentIndex()

        if domain_index == 0:
            domain = 'real-space'

        else:
            domain = 'k-space'

        if value_index == 0:
            value = 'real'

        elif value_index == 1:
            value = 'imag'

        elif value_index == 2:
            value = 'abs'

        elif value_index == 3:
            value = 'abs2'

        return (name, domain, dk3D, E_kin_max, value)

    def closeEvent(self, event):

        self.deleteLater()
        event.accept()

    def _setup(self):

        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
