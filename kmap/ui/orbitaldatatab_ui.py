from abc import abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QScrollArea)
from kmap.ui.abstract_ui import AbstractUI
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.crosshair import CrosshairAnnulus
from kmap.controller.colormap import Colormap
from kmap.controller.polarization import Polarization


class OrbitalDataTabUI(AbstractUI, QWidget):

    def _initialize_content(self):

        # Plot
        self.plot_item = PyQtGraphPlot()
        self.plot_item.setSizePolicy(
            QSP.Policy.Expanding, QSP.Policy.Expanding)

        # Top Spacer
        top_spacer = QSpacerItem(0, 0,
                                 hPolicy=QSP.Policy.Fixed,
                                 vPolicy=QSP.Policy.Fixed)

        # Crosshair
        self.crosshair = CrosshairAnnulus(self.plot_item)

        # Colormap
        self.colormap = Colormap(self.plot_item)

        # Polarisation
        self.polarization = Polarization()

        # Bottom Spacer
        bottom_spacer = QSpacerItem(0, 0,
                                    hPolicy=QSP.Policy.Fixed,
                                    vPolicy=QSP.Policy.Expanding)

        # Options Layout
        options_layout = QVBoxLayout()
        options_layout.addItem(top_spacer)
        options_layout.addWidget(self.crosshair)
        options_layout.addWidget(self.colormap)
        options_layout.addWidget(self.polarization)
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

        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.plot_item)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.crosshair.crosshair_changed.connect(self.crosshair_changed)

        self.polarization.polarization_changed.connect(
            self.polarization_changed)

    @abstractmethod
    def crosshair_changed(self):
        pass

    @abstractmethod
    def polarization_changed(self):
        pass
