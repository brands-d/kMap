# Python Imports
import logging
import traceback

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, QDir

# Own Imports
from kmap import __directory__
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.orbitaldatatab import OrbitalDataTab
from kmap.controller.profileplottab import ProfilePlotTab
from kmap.controller.lmfittab import LMFitTab
from kmap.controller.filetab import FileViewerTab, FileEditorTab
from kmap.library.qwidgetsub import Tab
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/tabwidget.ui')
TabWidget_UI, _ = uic.loadUiType(UI_file)


class TabWidget(QWidget, TabWidget_UI):

    tab_added = pyqtSignal(Tab)

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(TabWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def open_sliced_data_tab(self, path):
        # Opens a new sliced data tab

        log = logging.getLogger('kmap')
        log.info('Trying to load %s' % path)

        try:
            tab = SlicedDataTab.init_from_path(path)
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except Exception as e:

            log.error('Couldn\'t load %s' % path)
            log.error(traceback.format_exc())

    def open_sliced_data_tab_by_URL(self, URLs):

        try:
            tab = SlicedDataTab.init_from_URLs(URLs)
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except Exception as e:

            log = logging.getLogger('kmap')
            log.error('Couldn\'t load URLs')
            log.error(traceback.format_exc())

    def open_orbital_data_tab(self):
        # Opens a new orbital data tab

        tab = OrbitalDataTab()
        title = tab.get_title()

        self._open_tab(tab, title)

        return tab

    def open_file_tab(self, path, title, editable=False, richText=False):

        if editable:
            tab = FileEditorTab(path)
        else:
            tab = FileViewerTab(path, richText=richText)

        self._open_tab(tab, title)

    def open_lmfit_tab(self, sliced_tab, orbital_tab):

        tab = LMFitTab(sliced_tab.get_data(),orbital_tab.get_orbitals())

        self._open_tab(tab, 'LM-Fit Tab')

    def open_profile_tab(self):

        tab = ProfilePlotTab(self)

        self._open_tab(tab, 'Profile Plot')

    def get_orbital_tab_to_load_to(self):

        tab = None
        aux = self.tab_widget.currentWidget()
        if type(aux) == OrbitalDataTab:
            tab = aux

        else:
            for index in range(self.tab_widget.count()):
                aux = self.tab_widget.widget(index)

                if type(aux) == OrbitalDataTab:
                    tab = aux
                    break

        if tab is None:
            tab = self.open_orbital_data_tab()

        return tab

    def get_current_tab(self):

        return self.tab_widget.currentWidget()

    def get_tabs_of_type(self, type_):

        tabs = []

        for index in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(index)

            if type(tab) == type_ or type_ is None:
                tabs.append(tab)

        return tabs

    def close_tab(self, index):
        # Close tab specified with index

        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        widget.close()
        widget.deleteLater()

    def _open_tab(self, tab, title, tooltip=None):

        index = self.tab_widget.addTab(tab, title)
        self.tab_widget.setCurrentIndex(index)

        if tooltip is not None:
            self.tab_widget.setTabToolTip(index, tooltip)

        self.tab_added.emit(tab)

    def _connect(self):

        self.tab_widget.tabCloseRequested.connect(self.close_tab)
