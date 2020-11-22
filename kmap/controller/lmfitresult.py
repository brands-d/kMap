# Third Party Imports
from lmfit import fit_report

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ / 'ui/lmfitresult.ui'
LMFitResult_UI, _ = uic.loadUiType(UI_file)


class LMFitResult(QWidget, LMFitResult_UI):
    print_triggered = pyqtSignal()
    cov_matrix_requested = pyqtSignal()
    plot_requested = pyqtSignal()

    def __init__(self, result, lmfit_model):

        self.result = result

        # Setup GUI
        super(LMFitResult, self).__init__()
        self.setupUi(self)
        self._setup(lmfit_model)
        self._connect()

    def get_fit_report(self):

        return fit_report(self.result)

    def get_covariance_matrix(self):

        return self.result.covar

    def _setup(self, lmfit_model):

        slices = lmfit_model.slice_policy[1]

        if len(list(slices)) == 1:
            type_ = 'Only One Slice (%i)' % slices[0]
            self.plot_button.setEnabled(False)

        else:
            if lmfit_model.slice_policy[2]:
                type_ = 'All Slices Combined'
                self.plot_button.setEnabled(False)

            else:
                type_ = 'All Slices Individually'

        self.type_label.setText(type_)

    def _connect(self):

        self.result_button.clicked.connect(self.print_triggered.emit)
        self.correlation_button.clicked.connect(self.cov_matrix_requested.emit)
        self.plot_button.clicked.connect(self.plot_requested.emit)
