from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QScrollArea, QWidget)
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtCore import Qt
from map.ui.abstract_ui import AbstractUI
from map.view.pyqtgraphplot import PyQtGraphPlot
from map.view.dataslider import DataSlider


class SlicedDataTabUI(AbstractUI):

    def _initialize_content(self):

        options_widget = QWidget()
        # Options
        options_layout = QVBoxLayout()
        options_widget.setLayout(options_layout)
        options_widget.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)
        # Top Spacer
        options_layout.addItem(
            QSpacerItem(0, 0,
                        hPolicy=QSP.Policy.Fixed,
                        vPolicy=QSP.Policy.Fixed))

        # Slider
        self.slider = DataSlider(self.data)
        options_layout.addWidget(self.slider)
        self.slider.setSizePolicy(QSP.Policy.Expanding, QSP.Policy.Expanding)

        # Bottom Spacer
        options_layout.addItem(
            QSpacerItem(0, 0,
                        hPolicy=QSP.Policy.Fixed,
                        vPolicy=QSP.Policy.Expanding))
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidget(options_widget)
        scroll_area.setMinimumSize(0, 575)
        scroll_area.setSizePolicy(QSP.Policy.Maximum, QSP.Policy.Preferred)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Plot
        self.plot_item = PyQtGraphPlot()
        self.plot_item.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)

        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.plot_item)
        #main_layout.setStretch(0, 1)
        #main_layout.setStretch(1, 3)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.slider.value_changed.connect(self.change_slice)
