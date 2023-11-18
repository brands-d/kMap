from lmfit import fit_report
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.ui.lmfitresult import Ui_lmfitresult as LMFitResult_UI


class LMFitResult(QWidget, LMFitResult_UI):
    print_triggered = Signal()
    cov_matrix_requested = Signal()
    plot_requested = Signal()

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
            type_ = "Fitted Slice (%i)" % slices[0]
            self.plot_button.setEnabled(False)

        else:
            type_ = f"Fitted Slices {slices[0]}-{slices[-1]}"
            if lmfit_model.slice_policy[2]:
                type_ += " (Combined)"
                self.plot_button.setEnabled(False)

        self.type_label.setText(type_)

    def _connect(self):
        self.result_button.clicked.connect(self.print_triggered.emit)
        self.correlation_button.clicked.connect(self.cov_matrix_requested.emit)
        self.plot_button.clicked.connect(self.plot_requested.emit)
