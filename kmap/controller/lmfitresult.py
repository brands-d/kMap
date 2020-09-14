# Third Party Imports
from lmfit import fit_report

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfitresult.ui')
LMFitResult_UI, _ = uic.loadUiType(UI_file)


class LMFitResult(QWidget, LMFitResult_UI):

    def __init__(self, results):

        self.results = results

        # Setup GUI
        super(LMFitResult, self).__init__()
        self.setupUi(self)

    def get_index(self, index):

        try:
            return self.results[index]

        except IndexError:
            return self.results[0]
