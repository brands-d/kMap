import logging
from kmap.model.colormap_model import ColormapModel
from kmap.ui.colormap_ui import ColormapUI
from kmap.config.config import config
from kmap import __directory__


class Colormap(ColormapUI):

    def __init__(self, plot_item, path='/resources/misc/colormaps.json'):

        self.path = __directory__ + path
        self.model = ColormapModel(plot_item)

        ColormapUI.__init__(self)

        self.load_colormaps()

    def load_colormaps(self):

        self.model.load_colormaps(self.path)
        self._update_combobox()

        self._set_default_colormap()

    def _set_default_colormap(self):

        default_colormap = config.get_key('colormap', 'default')
        index = self.model.name_to_index(default_colormap)

        self.combobox.setCurrentIndex(index)
        self.change_colormap_by_index(index)

    def change_colormap_by_index(self, index):

        self.model.change_colormap(index)

    def add_colormap(self):

        name = self.lineEdit.text()

        if name == '':
            return
        else:
            self.model.add_colormap_from_plot(name)

        self.model.save_colormaps(self.path)

    def _update_combobox(self):

        self.combobox.blockSignals(True)
        self.combobox.clear()

        for colormap in self.model.colormaps:
            self.combobox.addItem(colormap.name)

        self.combobox.blockSignals(False)
