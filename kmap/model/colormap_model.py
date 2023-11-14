import json
import os

from pyqtgraph import ColorMap

from kmap.library.colormap import Colormap


class ColormapModel:
    def __init__(self, plot_item):
        self.colormaps = []

        if isinstance(plot_item, list):
            self.plot_item = plot_item

        else:
            self.plot_item = [plot_item]

    def load_colormaps(self, path):
        # Load colormaps from json file

        with open(path, "r") as file:
            data = json.loads(json.load(file))
            self.colormaps = []

            for colormap in data:
                name = colormap[0]
                pos = colormap[1]
                colors = colormap[2]

                self.add_colormap(name, pos, colors)

    def add_colormap_from_plot(self, name, ID=0):
        # Add current plot_item colormap as new colormap

        colormap = self.plot_item[ID].ui.histogram.gradient.colorMap()
        pos = colormap.pos.tolist()
        colors = colormap.getColors().tolist()

        self.add_colormap(name, pos, colors)

    def add_colormap(self, name, pos, colors):
        # Add new colormap to list of colormaps

        new_colormap = Colormap(name, pos, colors)
        self.colormaps.append(new_colormap)

    def remove_colormap(self, name):
        index = self._name_to_index(name)

        del self.colormaps[index]

    def save_colormaps(self, path):
        # Save colormaps in json file

        path_temp = path.parent / (path.name + ".temp")

        with open(path_temp, "w") as file:
            data = json.dumps([obj.toList() for obj in self.colormaps])
            json.dump(data, file)

        os.remove(path)
        os.rename(path_temp, path)

    def get_colormap(self, name):
        # Return a colormap by name

        for colormap in self.colormaps:
            if colormap.name == name:
                return colormap

        return None

    def set_current_colormap(self, name):
        # Change colormap of plot_item

        index = self._name_to_index(name)

        pos = self.colormaps[index].pos
        colors = self.colormaps[index].colors
        for plot_item in self.plot_item:
            plot_item.setColorMap(ColorMap(pos, colors))

    def _name_to_index(self, name):
        name_list = [colormap.name for colormap in self.colormaps]
        index = name_list.index(name)

        return index
