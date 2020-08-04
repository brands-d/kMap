from PyQt5.QtWidgets import QGroupBox, QLabel, QPushButton, QDoubleSpinBox
from PyQt5.QtCore import Qt
from kmap.ui.abstract_ui import AbstractUI


class OrbitalTableRowUI(AbstractUI, QGroupBox):

    def _initialize_misc(self):

        self.row = self.table.rowCount()
        self.table.insertRow(self.row)

    def _initialize_content(self):

        # Remove
        self.button = QPushButton('X')
        self.table.setCellWidget(self.row, 0, self.button)

        # ID
        label = QLabel(str(self.data_ID))
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.row, 1, label)

        # Name
        label = QLabel(self.data_name)
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.row, 2, label)

        # Deconvolution
        self.deconvolution = QDoubleSpinBox()
        self.deconvolution.setValue(1)
        self.deconvolution.setMinimum(-99999.9)
        self.deconvolution.setMaximum(99999.9)
        self.deconvolution.setDecimals(1)
        self.deconvolution.setSingleStep(0.1)
        self.deconvolution.setKeyboardTracking(False)
        self.table.setCellWidget(self.row, 3, self.deconvolution)

        # phi-Angle
        self.phi = QDoubleSpinBox()
        self.phi.setSuffix('°')
        self.phi.setValue(0)
        self.phi.setMinimum(-90)
        self.phi.setMaximum(90)
        self.phi.setDecimals(1)
        self.phi.setSingleStep(1)
        self.phi.setKeyboardTracking(False)
        self.table.setCellWidget(self.row, 4, self.phi)

        # theta-Angle
        self.theta = QDoubleSpinBox()
        self.theta.setSuffix('°')
        self.theta.setValue(0)
        self.theta.setMinimum(-90)
        self.theta.setMaximum(90)
        self.theta.setDecimals(1)
        self.theta.setSingleStep(1)
        self.theta.setKeyboardTracking(False)
        self.table.setCellWidget(self.row, 5, self.theta)

        # psi-Angle
        self.psi = QDoubleSpinBox()
        self.psi.setSuffix('°')
        self.psi.setValue(0)
        self.psi.setMinimum(-90)
        self.psi.setMaximum(90)
        self.psi.setDecimals(1)
        self.psi.setSingleStep(1)
        self.psi.setKeyboardTracking(False)
        self.table.setCellWidget(self.row, 6, self.psi)
