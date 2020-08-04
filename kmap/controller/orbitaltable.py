from kmap.ui.orbitaltable_ui import OrbitalTableUI
from kmap.controller.orbitaltablerow import OrbitalTableRow


class OrbitalTable(OrbitalTableUI):

    def __init__(self):

        self.rows = []

        OrbitalTableUI.__init__(self)

    def add_orbital(self, orbital):

        self._add_table_row(orbital.ID, orbital.name)

    def _add_table_row(self, ID, name):

        new_row = OrbitalTableRow(self, ID, name)
        self.rows.append(new_row)
