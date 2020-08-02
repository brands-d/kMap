import json
import os
import logging
import traceback
from pyqtgraph import ColorMap
from kmap.library.colormap import Colormap


class ColormapModel():

    def __init__(self, plot_item):

        self.colormaps = []
        self.plot_item = plot_item

    def load_colormaps(self, path):
        # Load colormaps from json file

        try:
            with open(path, 'r') as file:
                data = json.loads(json.load(file))

            self.colormaps = []
            for colormap in data:
                self.add_colormap(colormap[0], colormap[1], colormap[2])

        except Exception:

            log = logging.getLogger('kmap')

            log.error('Colormaps could not be loaded')
            log.error(traceback.format_exc())

    def name_to_index(self, name):

        index = 0
        found = False

        for index, colormap in enumerate(self.colormaps):
            if colormap.name == name:
                found = True
                break

        if not found:
            logging.getLogger('kmap').info(
                'Requested colormap %s not found. \
                Default to 0th colormap' % name)

        return index

    def add_colormap(self, name, pos, colors):
        # Add new colormap to list of colormaps

        self.colormaps.append(Colormap(name, pos, colors))

    def get_colormap(self, name):
        # Return a colormap by name

        for colormap in self.colormaps:
            if colormap.name == name:
                return colormap

        return None

    def change_colormap(self, index):
        # Change colormap of plot_item

        pos = self.colormaps[index].pos
        colors = self.colormaps[index].colors
        self.plot_item.setColorMap(ColorMap(pos, colors))

    def add_colormap_from_plot(self, name):
        # Add current plot_item colormap as new colormap

        colormap = self.plot_item.ui.histogram.gradient.colorMap()
        pos = colormap.pos.tolist()
        colors = colormap.getColors().tolist()

        self.add_colormap(name, pos, colors)

    def save_colormaps(self, path):
        # Save colormaps in json file

        path_temp = path + '.temp'

        try:
            with open(path_temp, 'w') as file:
                data = json.dumps([obj.toList() for obj in self.colormaps])
                json.dump(data, file)

            os.remove(path)
            os.rename(path_temp, path)

        except Exception:

            log = logging.getLogger('kmap')

            log.error('Colormaps could not be saved')
            log.error(traceback.format_exc())

            os.remove(path_temp)
