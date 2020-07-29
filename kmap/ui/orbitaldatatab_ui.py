from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QScrollArea)
from kmap.ui.abstract_ui import AbstractUI
from kmap.view.pyqtgraphplot import PyQtGraphPlot
from kmap.view.crosshair import CrosshairAnnulus
from kmap.view.colormap import Colormap


class OrbitalDataTabUI(AbstractUI):

    def _initialize_content(self):

        options_widget = QWidget()

        # Plot
        self.plot_item = PyQtGraphPlot()
        self.plot_item.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)

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

        # Crosshair
        self.crosshair = CrosshairAnnulus(self.plot_item)
        options_layout.addWidget(self.crosshair)

        # Colormap
        self.colormap = Colormap(self.plot_item)
        options_layout.addWidget(self.colormap)

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

        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.plot_item)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)
