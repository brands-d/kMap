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

    print_triggered = pyqtSignal()
    cov_matrix_requested = pyqtSignal()
    plot_requested = pyqtSignal()

    def __init__(self, results, type_, slice_index):

        self.results = results

        # Setup GUI
        super(LMFitResult, self).__init__()
        self.setupUi(self)
        self._setup(type_, slice_index)
        self._connect()

    def get_index(self, index):

        try:
            return self.results[index]

        except IndexError:
            return self.results[0]

    def get_fit_report(self, index):

        result = self.get_index(index)

        return fit_report(result)

    def get_covariance_matrix(self, index):

        result = self.get_index(index)
        # MinimizerResult has no covar?
        pass
        return result.covar

    def _setup(self, type_, slice_index):

        if type_ == 'Only One Slice':
            type_ = '%s (%i)' % (type_, slice_index)

        if type_ != 'All Slices Individually':
            self.plot_button.setEnabled(False)

        self.type_label.setText(type_)

    def _connect(self):

        self.result_button.clicked.connect(self.print_triggered.emit)
        self.correlation_button.clicked.connect(self.cov_matrix_requested.emit)
        self.plot_button.clicked.connect(self.plot_requested.emit)
