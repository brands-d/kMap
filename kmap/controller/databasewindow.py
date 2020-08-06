from PyQt5.QtCore import pyqtSignal
from kmap.ui.databasewindow_ui import DatabaseWindowUI
from kmap.library.database import Database


class DatabaseWindow(DatabaseWindowUI):

    file_chosen = pyqtSignal(str)

    def __init__(self, path):

        self.database = Database(path)
        self.URL = ''

        DatabaseWindowUI.__init__(self)

        self.show()

    def load_online(self):

        self.URL = self.lineedit.text()
        self._close()

    def load_database(self):

        URL_1 = self.database.URL

        molecule_number = self.molecule.value()
        molecule = self.database.molecules[molecule_number]
        URL_2 = molecule.URL

        orbital_number = self.orbital.value()
        orbital = molecule.orbitals[orbital_number]
        URL_3 = orbital.URL

        self.URL = URL_1 + URL_2 + URL_3

        self._close()

    def _close(self):

        print(self.URL)
        self.file_chosen.emit(self.URL)
        self.close()
