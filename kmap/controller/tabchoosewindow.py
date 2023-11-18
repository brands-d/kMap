from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow

from kmap.ui.tabchoosewindow import Ui_tabchoosewindow as TabChooseWindow_UI


class TabChooseWindow(QMainWindow, TabChooseWindow_UI):
    tabs_chosen = Signal(list)

    def __init__(self, sliced_tabs, orbital_tabs, *args, **kwargs):
        self.sliced_tabs = sliced_tabs
        self.orbital_tabs = orbital_tabs

        # Setup GUI
        super(TabChooseWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self._setup()
        self._connect()

        self.show()

    def choose_tabs(self):
        chosen_sliced_index = self.sliced_combobox.currentIndex()
        chosen_sliced_tab = self.sliced_tabs[chosen_sliced_index]

        chosen_orbital_index = self.orbital_combobox.currentIndex()
        chosen_orbital_tab = self.orbital_tabs[chosen_orbital_index]

        self.chosen_tabs = [chosen_sliced_tab, chosen_orbital_tab]

        self.close()

    def closeEvent(self, event):
        self.tabs_chosen.emit(self.chosen_tabs)
        self.deleteLater()
        event.accept()

    def _setup(self):
        for tab in self.sliced_tabs:
            self.sliced_combobox.addItem(tab.get_title())

        for tab in self.orbital_tabs:
            self.orbital_combobox.addItem(tab.get_title())

    def _connect(self):
        self.load.clicked.connect(self.choose_tabs)
