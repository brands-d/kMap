from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHeaderView, QMainWindow, QTreeWidgetItem

from kmap import __directory__
from kmap.config.config import config
from kmap.controller.slicedcubefileoptions import SlicedCubefileOptions
from kmap.controller.sliceddatabaseoptions import SlicedDataBaseOptions
from kmap.controller.sliceddatabaseoptions2 import SlicedDataBaseOptions2
from kmap.library.database import Database
from kmap.ui.databasewindow import Ui_main_window as DatabaseWindow_UI
from kmap.ui.sliceddatabasewindow import Ui_main_window as SlicedDatabaseWindow_UI


class DatabaseWindowBase(QMainWindow):
    files_chosen = Signal(list)

    def __init__(self):
        # Setup GUI
        super(DatabaseWindowBase, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def fill_tree(self):
        self.tree.clear()

        for molecule in self.database.molecules:
            if self._fit_filter(molecule):
                item = self.add_molecule(molecule)

    def add_molecule(self, molecule):
        molecule_item = MoleculeTreeWidgetItem(molecule)

        # Add the entries in the respective column
        entries = [
            "%i" % molecule.ID,
            molecule.full_name,
            molecule.formula,
            "%i" % molecule.charge,
            "%.3f" % molecule.magnetic_moment,
            molecule.XC_functional,
            "",
        ]

        for col, entry in enumerate(entries):
            molecule_item.setText(col, entry)
            molecule_item.setTextAlignment(col, Qt.AlignCenter)

        # Add item to tree
        self.tree.addTopLevelItem(molecule_item)

        # Add orbitals of molecule to tree
        for orbital in molecule.orbitals:
            self.add_orbital(orbital, molecule_item)

    def add_orbital(self, orbital, molecule_item):
        orbital_item = OrbitalTreeWidgetItem(orbital)

        # Add the entries in the respective column
        entries = [
            "%i" % orbital.ID,
            orbital.name,
            "",
            "",
            "",
            "",
            "%.3f" % orbital.energy,
        ]

        for col, entry in enumerate(entries):
            orbital_item.setText(col, entry)
            orbital_item.setTextAlignment(col, Qt.AlignCenter)

        # Add item to tree
        molecule_item.addChild(orbital_item)

    def find(self):
        search_text = self.line_edit.text()

        if not search_text:
            return

        items = self.tree.findItems(search_text, Qt.MatchFlag.MatchContains, 1)

        if not items:
            return

        current_item = self.tree.currentItem()
        if current_item in items:
            current_index = items.index(current_item)
            next_index = (current_index + 1) % len(items)

        else:
            next_index = 0

        next_item = items[next_index]
        self.tree.setCurrentItem(next_item)

    def load_database(self):
        orbitals_chosen = self._get_chosen_orbitals()

        for orbital in orbitals_chosen:
            URL = orbital.URL
            meta_data = orbital.get_meta_data()
            self.URLs.append([URL, meta_data])

        self.close()

    def closeEvent(self, event):
        self.files_chosen.emit(self.URLs)
        self.deleteLater()
        event.accept()

    def _setup_tree(self):
        header_labels = [
            "ID",
            "Name",
            "Formula",
            "Charge",
            "Mag. Moment",
            "XC-Funktional",
            "Energy",
        ]
        self.tree.setHeaderLabels(header_labels)
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(2, 150)
        self.tree.setColumnWidth(3, 100)
        self.tree.setColumnWidth(4, 150)
        self.tree.setColumnWidth(5, 150)
        self.tree.setColumnWidth(6, 120)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)
        self.tree.header().setSectionResizeMode(1, QHeaderView.Stretch)

        self.tree.sortItems(0, Qt.SortOrder.AscendingOrder)

    def _fit_filter(self, molecule):
        filter_ = self.combobox.currentText()

        if filter_ == "No Filter" or molecule.XC_functional == filter_:
            return True

        else:
            return False

    def _get_chosen_orbitals(self):
        orbitals = []

        selected_items = self.tree.selectedItems()

        for selected_item in selected_items:
            # Top level items have no parent and are molecules
            if not selected_item.parent():
                molecule = selected_item.molecule

                for orbital in molecule.orbitals:
                    orbitals.append(orbital)

            else:
                orbital = selected_item.orbital
                orbitals.append(orbital)

        # Set removes duplicates from selecting molecule and orbitals
        return set(orbitals)

    def _connect(self):
        self.combobox.currentTextChanged.connect(self.fill_tree)

        self.database_load_button.clicked.connect(self.load_database)
        self.find_button.clicked.connect(self.find)


class OrbitalDatabase(DatabaseWindowBase, DatabaseWindow_UI):
    def __init__(self, *args, **kwargs):
        super(OrbitalDatabase, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup_tree()
        self._connect()

        # Setup database
        path = __directory__ / config.get_key("paths", "database")
        self.database = Database(path)

        # URLs (with extra information if available) chosen
        self.URLs = []

        self.fill_tree()

        self.show()

    def load_urls(self):
        text = self.text_edit.toPlainText()

        # Nothing entered
        if not text:
            self.URLs = []

        # Multiple URLs entered
        elif "\n" in text:
            self.URLs = text.split("\n")

        # Only one URL entered
        else:
            self.URLs.append([text, {}])

        self.close()

    def _connect(self):
        DatabaseWindowBase._connect(self)

        self.url_load_button.clicked.connect(self.load_urls)


class SlicedDatabaseWindow(DatabaseWindowBase, SlicedDatabaseWindow_UI):
    def __init__(self, mode, *args, **kwargs):
        super(SlicedDatabaseWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup_tree()
        self._connect()

        # Setup database
        path = __directory__ / config.get_key("paths", "database")
        self.database = Database(str(path))

        # Open Options Window
        if mode == "binding-energy":
            self.options = SlicedDataBaseOptions()

        elif mode == "photon-energy":
            self.options = SlicedDataBaseOptions2()

        elif mode == "cubefile":
            self.options = SlicedCubefileOptions()

        # URLs (with extra information if available) chosen
        self.URLs = []

        self.fill_tree()

        self.show()
        self.options.show()

    def load_database(self):
        orbitals_chosen = self._get_chosen_orbitals()

        for orbital in orbitals_chosen:
            URL = orbital.URL
            meta_data = orbital.get_meta_data()
            options = self.options.get_parameters()
            self.URLs.append([URL, meta_data])

        self.URLs.append(options)

        self.close()

    def closeEvent(self, event):
        DatabaseWindowBase.closeEvent(self, event)

        try:
            self.options.deleteLater()

        except RuntimeError:
            pass


class TreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()

        self_string = self.text(column).lower()
        other_string = other.text(column).lower()

        if self_string.isnumeric() and other_string.isnumeric():
            return float(self_string) < float(other_string)

        else:
            return self_string < other_string


class MoleculeTreeWidgetItem(TreeWidgetItem):
    def __init__(self, molecule, *args, **kwargs):
        self.molecule = molecule

        super(MoleculeTreeWidgetItem, self).__init__(*args, **kwargs)


class OrbitalTreeWidgetItem(TreeWidgetItem):
    def __init__(self, orbital, *args, **kwargs):
        self.orbital = orbital

        super(OrbitalTreeWidgetItem, self).__init__(*args, **kwargs)
