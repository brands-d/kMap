from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtCore import Qt
from map.config.config import config


class DataSliderUI(AbstractUI):

    def _initialize_content(self):

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Label
        if 'slice_keys' in self.data.meta_data:
            slice_keys = self.data.meta_data['slice_keys']

        else:
            slice_keys = config.get_key('sliced_data', 'default_slice_keys')

        if 'slice_unit' in self.data.meta_data:
            unit = self.data.meta_data['slice_unit']

        else:
            unit = config.get_key('sliced_data', 'default_slice_unit')
        self.label = QLabel('<b>' + slice_keys + ' [' + unit + ']:' + '</b>')
        self.label.setSizePolicy(QSP.Policy.Maximum, QSP.Policy.Maximum)
        top_layout.addWidget(self.label)
        # Value label
        self.value_label = QLabel('')
        self.value_label.setSizePolicy(
            QSP.Policy.Preferred, QSP.Policy.Preferred)
        self.value_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(self.value_label)
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        main_layout.addWidget(self.slider) 

    def _initialize_connections(self):

        self.slider.valueChanged.connect(self.change_slice)
