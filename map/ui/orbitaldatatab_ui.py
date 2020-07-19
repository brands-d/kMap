from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox
from map.view.pyqtgraphplot import PyQtGraphPlot


class OrbitalDataTabUI(AbstractUI):

    def _initialize_content(self):

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Plot
        self.plot_item = PyQtGraphPlot()
        main_layout.addWidget(self.plot_item)
