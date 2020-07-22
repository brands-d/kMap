from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtCore import Qt


class DataSliderUI(AbstractUI):

    def _initialize_content(self):

        self.setTitle('Slices')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

        # Key Label
        self.key_label = QLabel('')
        self.key_label.setSizePolicy(QSP.Policy.Maximum, QSP.Policy.Maximum)

        # Value label
        self.value_label = QLabel('')
        self.value_label.setSizePolicy(
            QSP.Policy.Preferred, QSP.Policy.Preferred)
        self.value_label.setAlignment(Qt.AlignRight)

        # Top Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.key_label)
        top_layout.addWidget(self.value_label)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimumSize(10, 30)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.slider)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.slider.valueChanged.connect(self.change_slice)
