from map.ui.orbitaldatatab_ui import OrbitalDataTabUI
from PyQt5.QtWidgets import QWidget


class OrbitalDataTab(QWidget, OrbitalDataTabUI):

    def __init__(self, model, orbital):

        super().__init__()

        self.setupUi(model)

        self.plot_item.plot(orbital.get_kmap(E_kin=50, phi=10, Ak_type='toroid'))
