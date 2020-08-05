from abc import abstractmethod
from PyQt5.QtCore import pyqtSignal
from kmap.ui.tablerow_ui import OrbitalTableRowUI


class TableRow():

    row_removed = pyqtSignal(int)
    parameter_changed = pyqtSignal(int, str, float)

    def __init__(self, table, data_ID, data_name):

        self.table = table
        self.ID = data_ID
        self.name = data_name
        self.widgets = []

    def remove_row(self):

        self.row_removed.emit(self.ID)

    def get_parameters(self):

        parameters = []
        for widget in self.widgets:
            parameters.append(widget.value())

        return parameters

    def change_parameter(self):

        sender = self.sender()

        ID_ = self.ID
        parameter = sender.objectName()
        value = sender.value()

        self.parameter_changed.emit(ID_, parameter, value)

    def update_parameter_silently(self, parameter, value):

        for widget in self.widgets:
            if widget.objectName() == parameter:

                widget.blockSignals(True)
                widget.setValue(value)
                widget.blockSignals(False)


class OrbitalTableRow(TableRow, OrbitalTableRowUI):

    def __init__(self, parent, data_ID, data_name):

        TableRow.__init__(self, parent, data_ID, data_name)
        OrbitalTableRowUI.__init__(self)

        self.widgets = [self.deconvolution, self.phi, self.theta, self.psi]
