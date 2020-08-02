from abc import abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QScrollArea)
from kmap.config.config import config
from kmap.ui.abstract_ui import AbstractUI
from kmap.controller.dataslider import DataSlider
from kmap.controller.crosshair import CrosshairAnnulus
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.colormap import Colormap


class SlicedDataTabUI(AbstractUI, QWidget):

    def _initialize_content(self):

        # Plot
        self.plot_item = PyQtGraphPlot()
        self.plot_item.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)
        
        # Top Spacer
        top_spacer = QSpacerItem(
            0, 0, hPolicy=QSP.Policy.Fixed, vPolicy=QSP.Policy.Fixed)

        # Slider
        self.slider = DataSlider(self.model.data)

        # Crosshair
        self.crosshair = CrosshairAnnulus(self.plot_item)

        # Colormap
        self.colormap = Colormap(self.plot_item)

        # Bottom Spacer
        bottom_spacer = QSpacerItem(
            0, 0, hPolicy=QSP.Policy.Fixed, vPolicy=QSP.Policy.Expanding)

        # Options Layout
        options_layout = QVBoxLayout()
        options_layout.addItem(top_spacer)
        options_layout.addWidget(self.slider)
        options_layout.addWidget(self.crosshair)
        options_layout.addWidget(self.colormap)
        options_layout.addItem(bottom_spacer)

        # Options Widget
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        options_widget.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidget(options_widget)
        scroll_area.setMinimumSize(0, 625)
        scroll_area.setSizePolicy(QSP.Policy.Maximum, QSP.Policy.Preferred)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.plot_item)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
        self.slider.value_changed.connect(self.change_slice)

    @abstractmethod
    def crosshair_changed(self, name):
        pass

    @abstractmethod
    def change_slice(self):
        pass


'''# Slider
        if 'slice_keys' in self.data.meta_data:
            key_label = self.data.meta_data['slice_keys']

        else:
            key_label = config.get_key('sliced_data', 'default_slice_keys')

        if 'slice_unit' in self.data.meta_data:
            unit = self.data.meta_data['slice_unit']

        else:
            unit = config.get_key('sliced_data', 'default_slice_unit')

        self.slider = DataSlider(self.data.slice_keys,
                                 key_label=key_label, unit=unit)'''
