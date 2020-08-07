from PyQt5.QtCore import pyqtSignal
from kmap.ui.databasewindow_ui import DatabaseWindowUI
from kmap.library.database import Database


class DatabaseWindow(DatabaseWindowUI):

    files_chosen = pyqtSignal(list)

    def __init__(self, path):

        self.database = Database(path)
        self.URLs = []
        self.filter = 'No Filter'

        DatabaseWindowUI.__init__(self)

        self._fill_tree()

        self.show()

    def load_urls(self):

        text = self.line_edit.toPlainText()

        if not text:
            self.URLs = []

        elif '\n' in text:
            self.URLs = text.split('\n')

        else:
            self.URLs.append(text)

        self._close()

    def load_database(self):

        orbitals_chosen = self.tree.get_chosen_items()

        for orbital in orbitals_chosen:
            URL = self.database.URL
            URL = URL + orbital.molecule.URL
            URL = URL + orbital.URL
            self.URLs.append(URL)

        self._close()

    def filter_tree(self):

        self.filter = self.combobox.currentText()
        self._fill_tree()

    def _fill_tree(self, ):

        self.tree.clear()

        for molecule in self.database.molecules:
            if self._fit_filter(molecule):
                item = self.tree.add_molecule(molecule)

    def _fit_filter(self, molecule):

        if self.filter == 'No Filter':
            return True

        elif molecule.XC_functional == self.filter:
            return True

        else:
            return False

    def _close(self):

        print(self.URLs)
        self.files_chosen.emit(self.URLs)
        self.close()
