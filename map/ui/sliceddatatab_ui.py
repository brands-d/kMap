from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox

import pyqtgraph as pg


class SlicedDataTabUI(AbstractUI):

    def _initialize_content(self):

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Plot
        self.plot_item = pg.ImageView(view=pg.PlotItem())
        main_layout.addWidget(self.plot_item)