from map.ui.sliceddatatab_ui import SlicedDataTabUI
from PyQt5.QtWidgets import QWidget


class SlicedDataTab(QWidget, SlicedDataTabUI):

    def __init__(self, model, data):

        super().__init__()

        self.setupUi(model)

        self.plot(data)

    def plot(self, data):

        image = data.slice_from_idx(0)
        pos = image.range[:, 0]
        scale = image.step_size
        self.plot_item.clear()
        self.plot_item.setImage(image.data)
        #self.plot_item.setImage(image.data, autoRange=True, autoLevels=True,
        #                   axes={'x': 0, 'y': 1}, pos=pos, scale=scale)
