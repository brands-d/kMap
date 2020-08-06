from abc import abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QPushButton, QDoubleSpinBox,
    QCheckBox, QHBoxLayout, QWidget)
from kmap.ui.abstract_ui import AbstractUI


class OrbitalTableRowUI(AbstractUI, QGroupBox):

    def _initialize_content(self):

        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        # Remove
        self.button = QPushButton('X')

        # ID
        ID_label = QLabel(str(self.ID))
        ID_label.setAlignment(Qt.AlignCenter)

        # Name
        name_label = QLabel(self.name)
        name_label.setAlignment(Qt.AlignCenter)

        # Weight
        self.weight = QDoubleSpinBox()
        self.weight.setValue(1)
        self.weight.setMinimum(-99999.9)
        self.weight.setMaximum(99999.9)
        self.weight.setDecimals(1)
        self.weight.setSingleStep(0.1)
        self.weight.setKeyboardTracking(False)
        self.weight.setObjectName('weight')

        # Phi-Angle
        self.phi = QDoubleSpinBox()
        self.phi.setSuffix('°')
        self.phi.setValue(0)
        self.phi.setMinimum(-90)
        self.phi.setMaximum(90)
        self.phi.setDecimals(1)
        self.phi.setSingleStep(1)
        self.phi.setKeyboardTracking(False)
        self.phi.setObjectName('phi')

        # Theta-Angle
        self.theta = QDoubleSpinBox()
        self.theta.setSuffix('°')
        self.theta.setValue(0)
        self.theta.setMinimum(-90)
        self.theta.setMaximum(90)
        self.theta.setDecimals(1)
        self.theta.setSingleStep(1)
        self.theta.setKeyboardTracking(False)
        self.theta.setObjectName('theta')

        # Psi-Angle
        self.psi = QDoubleSpinBox()
        self.psi.setSuffix('°')
        self.psi.setValue(0)
        self.psi.setMinimum(-90)
        self.psi.setMaximum(90)
        self.psi.setDecimals(1)
        self.psi.setSingleStep(1)
        self.psi.setKeyboardTracking(False)
        self.psi.setObjectName('psi')

        # Use Checkbox
        self.use = QCheckBox('')
        self.use.setChecked(True)

        # Layout to center Checkbox
        layout = QHBoxLayout()
        layout.addWidget(self.use)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        # Widget to embed layout into
        widget = QWidget()
        widget.setLayout(layout)

        # Embed Widget in Table
        self.table.setCellWidget(row_index, 0, self.button)
        self.table.setCellWidget(row_index, 1, ID_label)
        self.table.setCellWidget(row_index, 2, name_label)
        self.table.setCellWidget(row_index, 3, self.weight)
        self.table.setCellWidget(row_index, 4, self.phi)
        self.table.setCellWidget(row_index, 5, self.theta)
        self.table.setCellWidget(row_index, 6, self.psi)
        self.table.setCellWidget(row_index, 7, widget)

    def _initialize_connections(self):

        self.button.clicked.connect(self.remove_row)

        self.weight.valueChanged.connect(self.change_parameter)
        self.phi.valueChanged.connect(self.change_parameter)
        self.theta.valueChanged.connect(self.change_parameter)
        self.psi.valueChanged.connect(self.change_parameter)

        self.use.stateChanged.connect(self.change_use)

    @abstractmethod
    def remove_row(self):
        pass

    @abstractmethod
    def change_parameter(self):
        pass
