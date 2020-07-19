from map.ui.orbitaldatatab_ui import OrbitalDataTabUI
from PyQt5.QtWidgets import QWidget


class OrbitalDataTab(QWidget, OrbitalDataTabUI):

    def __init__(self, model, orbital):

        super().__init__()

        self.setupUi(model)

        self.plot(orbital.get_kmap(E_kin=50, phi=10, Ak_type='toroid'))

    def plot(self, plotdata, pixel_center=True):

        image = plotdata.data
        scale = plotdata.step_size
        '''Move image position by half a step to make center of pixel
        the point specified by axis'''
        if pixel_center:
            pos = plotdata.range[:, 0] - scale / 2

        else:
            pos = plotdata.range[:, 0]

        self.plot_item.setImage(image, autoRange=True,
                                autoLevels=True, pos=pos, scale=scale)
