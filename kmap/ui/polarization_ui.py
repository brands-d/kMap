from abc import abstractmethod
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QComboBox, QDoubleSpinBox, QGridLayout)
from kmap.ui.abstract_ui import AbstractUI


class PolarizationUI(AbstractUI, QGroupBox):

    def _initialize_misc(self):

        self.setTitle('Polarisation')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

    def _initialize_content(self):

        # Polarisation Label
        polarisation_label = QLabel('Polarisation:')

        # Polarisation Combobox
        self.combobox = QComboBox()
        self.combobox.setDuplicatesEnabled(False)
        self.combobox.addItem('no |A\u2096|\u00B2')
        self.combobox.addItem('Toroid (p-pol)')
        self.combobox.addItem('NANO-ESCA: p-pol')
        self.combobox.addItem('NANO-ESCA: s-pol')
        self.combobox.addItem('NANO-ESCA: circ+')
        self.combobox.addItem('NANO-ESCA: circ-')
        self.combobox.addItem('NANO-ESCA: CDAD')

        # angle Label
        angle_label = QLabel('Angle of Incidence:')

        # Angle Spinbox
        self.angle_spinbox = QDoubleSpinBox()
        self.angle_spinbox.setKeyboardTracking(False)
        self.angle_spinbox.setSuffix('°')
        self.angle_spinbox.setMinimum(0)
        self.angle_spinbox.setMaximum(90)
        self.angle_spinbox.setDecimals(1)
        self.angle_spinbox.setSingleStep(1)

        # Azimuth Label
        azimuth_label = QLabel('Azimuth of Incidence:')

        # Azimuth Spinbox
        self.azimuth_spinbox = QDoubleSpinBox()
        self.azimuth_spinbox.setKeyboardTracking(False)
        self.azimuth_spinbox.setSuffix('°')
        self.azimuth_spinbox.setMinimum(0)
        self.azimuth_spinbox.setMaximum(360)
        self.azimuth_spinbox.setDecimals(1)
        self.azimuth_spinbox.setSingleStep(1)

        # Layout
        layout = QGridLayout()
        layout.addWidget(polarisation_label, 0, 0)
        layout.addWidget(self.combobox, 0, 1)
        layout.addWidget(angle_label, 1, 0)
        layout.addWidget(self.angle_spinbox, 1, 1)
        layout.addWidget(azimuth_label, 2, 0)
        layout.addWidget(self.azimuth_spinbox, 2, 1)

        self.setLayout(layout)

    def _initialize_connections(self):

        self.combobox.currentIndexChanged.connect(self.change_polarization)
        self.angle_spinbox.valueChanged.connect(self.change_polarization)
        self.azimuth_spinbox.valueChanged.connect(self.change_polarization)

    @abstractmethod
    def change_polarization(self):
        pass
