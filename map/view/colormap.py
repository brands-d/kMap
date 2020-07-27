import json
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal
from map.ui.colormap_ui import ColormapUI
from map import __directory__


class Colormap(ColormapUI):

    def __init__(self, plot_item):

        self.plot_item = plot_item

        super().__init__()
        self.setupUI()

        self.load_colormaps()
        self.change_colormap(self.combobox.itemText(0))

    def load_colormaps(self):

        with open(__directory__ + '/resources/misc/colormaps.json',
                  'r') as file:
            self.colormaps = json.loads(json.load(file))

        self.combobox.blockSignals(True)

        self.combobox.clear()
        for key in self.colormaps:
            self.combobox.addItem(key)

        self.combobox.blockSignals(False)

    def change_colormap(self, name):

        colormap = self.colormaps[name]
        self.plot_item.setColorMap(pg.ColorMap(colormap[0], colormap[1]))

    def add_colormap(self):

        name = self.add_lineEdit.text()

        if self.add_lineEdit.text() == '':
            return

        pos = self.plot_item.ui.histogram.gradient.colorMap().pos
        colors = self.plot_item.ui.histogram.gradient.colorMap().getColors()

        self.colormaps.update({name: [pos.tolist(), colors.tolist()]})

        with open(__directory__ + '/resources/misc/colormaps.json',
                  'w') as file:
            json.dump(json.dumps(self.colormaps), file)

        self.load_colormaps()
