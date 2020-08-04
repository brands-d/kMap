from kmap.ui.orbitaltablerow_ui import OrbitalTableRowUI


class OrbitalTableRow(OrbitalTableRowUI):

    def __init__(self, parent, data_ID, data_name):

        self.table = parent.table
        self.data_ID = data_ID
        self.data_name = data_name

        OrbitalTableRowUI.__init__(self)
