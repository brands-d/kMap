# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitTab_UI, _ = uic.loadUiType(UI_file)


class LMFitTab(QWidget, LMFitTab_UI):

    def __init__(self):

        # Setup GUI
        super(LMFitTab, self).__init__()
        self.setupUi(self)
