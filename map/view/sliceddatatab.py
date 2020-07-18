from map.ui.sliceddatatab_ui import SlicedDataTabUI
from PyQt5.QtWidgets import QWidget


class SlicedDataTab(QWidget, SlicedDataTabUI):

    def __init__(self, model, data):

        super().__init__()

        self.setupUi(model)

        self.plot(data.slice_from_idx(0))

    def plot(self, plotdata, pixel_center=True):

        image = plotdata.data
        scale = plotdata.step_size
        '''Move image position by half a step to make center of pixel
        the point specified by axis'''
        if pixel_center:
            pos = plotdata.range[:, 0] - scale / 2

        else:
            pos = plotdata.range[:, 0]
            
        self.plot_item.clear()
        self.plot_item.setImage(image, autoRange=True, autoLevels=True,
                                axes={'x': 0, 'y': 1}, pos=pos, scale=scale)
