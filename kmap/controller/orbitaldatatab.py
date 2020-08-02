import logging
from PyQt5.QtWidgets import QWidget
from kmap.library.misc import get_ID_from_tab_text
from kmap.ui.orbitaldatatab_ui import OrbitalDataTabUI


class OrbitalDataTab(OrbitalDataTabUI):

    def __init__(self):

        self.model = OrbitalDataTabModel(self)

        OrbitalDataTabUI.__init__(self)

        self.change_slice(0)

    def get_parameters(self):

        return None

    def crosshair_changed(self):
        pass