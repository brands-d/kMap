import datetime
import logging
import traceback

import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from kmap.config.config import config
from kmap.controller.filetab import FileEditorTab, FileViewerTab
from kmap.controller.lmfitplottab import LMFitPlotTab
from kmap.controller.lmfittab import LMFitResultTab, LMFitTab
from kmap.controller.orbitaldatatab import OrbitalDataTab
from kmap.controller.profileplottab import ProfilePlotTab
from kmap.controller.renametabwindow import RenameTabWindow
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.splitviewtab import SplitViewTab
from kmap.library.qwidgetsub import Tab
from kmap.ui.tabwidget import Ui_tabwidget as TabWidget_UI


class TabWidget(QWidget, TabWidget_UI):
    tab_added = Signal(Tab)

    def __init__(self, *args, **kwargs):
        self.ID_counter = -1

        # Setup GUI
        super(TabWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def open_sliced_data_tab(self, path):
        # Opens a new sliced data tab

        log = logging.getLogger("kmap")
        log.info("Trying to load %s" % str(path))

        try:
            tab = SlicedDataTab.init_from_path(str(path))
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except Exception as e:
            log.error("Couldn't load %s" % str(path))
            log.error(traceback.format_exc())

    def open_sliced_data_tab_by_URLs(self, URLs):
        try:
            tab = SlicedDataTab.init_from_URLs(URLs)
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except ValueError as e:
            pass

        except Exception as e:
            log = logging.getLogger("kmap")
            log.error("Couldn't load URLs")
            log.error(traceback.format_exc())

    def open_sliced_data_tab_by_URL(self, URL):
        try:
            tab = SlicedDataTab.init_from_URL(URL)
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except ValueError as e:
            pass

        except Exception as e:
            log = logging.getLogger("kmap")
            log.error("Couldn't load URL")
            log.error(traceback.format_exc())

    def open_sliced_data_tab_by_cube(self, URL):
        try:
            tab = SlicedDataTab.init_from_cube(URL)
            title = tab.get_title()
            tooltip = tab.to_string()
            self._open_tab(tab, title, tooltip)

        except ValueError as e:
            pass

        except Exception as e:
            log = logging.getLogger("kmap")
            log.error("Couldn't load cube file")
            log.error(traceback.format_exc())

    def open_orbital_data_tab(self):
        # Opens a new orbital data tab

        tab = OrbitalDataTab()
        tab.get_energy.connect(self.get_sliced_energy)
        title = tab.get_title()

        self._open_tab(tab, title)

        return tab

    def get_sliced_energy(self):
        match_type = config.get_key("orbital", "match_type")
        tabs = self.get_tabs_of_type(SlicedDataTab)
        if tabs:
            axis_idx = tabs[0].get_axis()
            axis = tabs[0].get_data().axes[axis_idx]
            if match_type == "average":
                energy = np.nanmean(axis.axis)
            elif match_type == "max":
                energy = max(axis.axis)
            elif match_type == "min":
                energy = min(axis.axis)
            else:
                slice = tabs[0].get_slice()
                energy = axis.axis[slice]

            self.sender().change_kinetic_energy(energy)

    def open_file_tab(self, path, title, editable=False, richText=False):
        if editable:
            tab = FileEditorTab(path, title)
        else:
            tab = FileViewerTab(path, title, richText=richText)

        self._open_tab(tab, title)

    def open_split_view_tab(self, sliced_tab, orbital_tab, save=None):
        if save is None:
            tab = SplitViewTab(sliced_tab, orbital_tab)

        else:
            tab = SplitViewTab.init_from_save(save, sliced_tab, orbital_tab)

        tab.locked_tabs = [sliced_tab, orbital_tab]
        sliced_tab.lock_while_open(tab)
        orbital_tab.lock_while_open(tab)
        tab.sliced_data_tab = sliced_tab
        tab.orbital_data_tab = orbital_tab

        self._open_tab(tab, "Split View")

        return tab

    def open_lmfit_tab(self, sliced_tab, orbital_tab, save=None):
        if save is None:
            tab = LMFitTab(sliced_tab, orbital_tab)
            tab.title = "LM-Fit Tab"

        else:
            tab = LMFitTab.init_from_save(save, sliced_tab, orbital_tab)
        tab.fit_finished.connect(self.open_result_tab)
        tab.locked_tabs = [sliced_tab, orbital_tab]

        sliced_tab.lock_while_open(tab)
        orbital_tab.lock_while_open(tab)
        tab.sliced_data_tab = sliced_tab
        tab.orbital_data_tab = orbital_tab

        self._open_tab(tab, "LM-Fit Tab")

        return tab

    def open_result_tab(self, *args, sender=None, save=None, ID_map=None):
        lmfit_tab = self.sender() if sender is None else sender
        if save is None:
            tab = LMFitResultTab(lmfit_tab, *args)
        else:
            tab = LMFitResultTab.init_from_save(save, lmfit_tab, ID_map)

        tab.open_plot_tab.connect(self.open_lmfit_plot_tab)
        tab.locked_tabs = [lmfit_tab]

        lmfit_tab.lock_while_open(tab)

        current_time = datetime.datetime.now()
        title = "Results (%i:%i)" % (current_time.hour, current_time.minute)
        tab.set_title(title)
        self._open_tab(tab, title)

        return tab

    def open_lmfit_plot_tab(self, *args, sender=None, save=None):
        result_tab = self.sender() if sender is None else sender

        if save is None:
            tab = LMFitPlotTab(*args, result_tab)

        else:
            tab = LMFitPlotTab.init_from_save(save, result_tab)

        tab.locked_tabs = [result_tab]

        result_tab.lock_while_open(tab)

        title = "Plot"
        tab.set_title(title)
        self._open_tab(tab, title)

        return tab

    def open_profile_tab(self):
        tab = ProfilePlotTab(self, "Profile Plot")

        self._open_tab(tab, "Profile Plot")

        return tab

    def get_index_of(self, tab):
        return self.tab_widget.indexOf(tab)

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

    def get_all_tabs(self):
        count = self.tab_widget.count()
        tabs = [self.tab_widget.widget(i) for i in range(count)]
        tabs = [tab for tab in tabs if tab.title != "Welcome"]
        return tabs

    def get_tabs_of_type(self, type_):
        tabs = []

        for index in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(index)

            if type(tab) == type_ or type_ is None:
                tabs.append(tab)

        return tabs

    def rename_current_tab(self):
        self.rename_tab = RenameTabWindow()
        self.rename_tab.title_chosen.connect(self.set_tab_title)

    def get_tab_by_ID(self, ID):
        tabs = self.get_all_tabs()
        for tab in tabs:
            if tab.ID == ID:
                return tab

        raise Exception("Tab not found")

    def set_tab_title(self, title):
        current_tab = self.get_current_tab()
        current_tab_index = self.tab_widget.indexOf(current_tab)

        current_tab.set_title(title)
        self.tab_widget.setTabText(current_tab_index, title)

        for tab in self.get_tabs_of_type(ProfilePlotTab):
            tab.rename_loaded_tab(current_tab, title)

    def duplicate_tab(self):
        current_tab = self.get_current_tab()

        if current_tab is None:
            return

        save = current_tab.save_state()

        if isinstance(current_tab, ProfilePlotTab):
            tab = self.open_profile_tab()
            tab.restore_state(save)

        elif isinstance(current_tab, OrbitalDataTab):
            tab = self.open_orbital_data_tab()
            tab.restore_state(save[0])

        elif isinstance(current_tab, SlicedDataTab):
            tab, _ = SlicedDataTab.init_from_save(save[0])

        elif isinstance(current_tab, LMFitResultTab):
            tab = self.open_result_tab(sender=save[1][0], save=save[0])

        elif isinstance(current_tab, LMFitTab):
            tab = self.open_lmfit_tab(*save[1], save=save[0])

        elif isinstance(current_tab, SplitViewTab):
            tab = self.open_split_view_tab(*save[1], save=save[0])

        elif isinstance(current_tab, LMFitPlotTab):
            tab = self.open_lmfit_plot_tab(sender=save[1][0], save=save[0])

        else:
            tab = type(current_tab).init_from_save(save[0])

        title = tab.get_title()
        tab.set_title(title)
        self._open_tab(tab, title)

    def open_tab_by_save(self, tab_save):
        class_, ID, title, save_, dependencies = tab_save
        if class_ == "SlicedDataTab":
            tab = SlicedDataTab.init_from_save(save_, dependencies)

        elif class_ == "OrbitalDataTab":
            tab = OrbitalDataTab.init_from_save(save_, dependencies)

        elif class_ == "SplitViewTab":
            tab = SplitViewTab.init_from_save(save_, dependencies, self)
            sliced_tab, orbital_tab = tab.locked_tabs
            sliced_tab.lock_while_open(tab)
            orbital_tab.lock_while_open(tab)

        elif class_ == "ProfilePlotTab":
            tab = ProfilePlotTab.init_from_save(save_, dependencies, self)

        elif class_ == "LMFitTab":
            tab = LMFitTab.init_from_save(save_, dependencies, self)

            tab.fit_finished.connect(self.open_result_tab)
            sliced_tab, orbital_tab = tab.locked_tabs
            sliced_tab.lock_while_open(tab)
            orbital_tab.lock_while_open(tab)

        elif class_ == "LMFitResultTab":
            tab = LMFitResultTab.init_from_save(save_, dependencies, self)

            lmfittab = tab.locked_tabs[0]
            lmfittab.lock_while_open(tab)
            tab.open_plot_tab.connect(self.open_lmfit_plot_tab)

        elif class_ == "LMFitPlotTab":
            tab = LMFitPlotTab.init_from_save(save_, dependencies, self)

            lmfitresulttab = tab.locked_tabs[0]
            lmfitresulttab.lock_while_open(tab)

        else:
            print("ERROR: Invalid save file")
            return

        tab.set_title(title)
        tab.set_ID(ID)
        self._open_tab(tab, title, ID=ID)

    def close_tab(self, index):
        # Close tab specified with index

        widget = self.tab_widget.widget(index)

        if widget.lock_tab is None:
            for tab in widget.locked_tabs:
                tab.unlock()

            self.tab_widget.removeTab(index)
            widget.close()
            widget.deleteLater()

        else:
            log = logging.getLogger("kmap")
            log.warning("Tab is locked open because different tab still references it.")

    def save_state(self):
        all_tabs = self.get_all_tabs()
        tab_saves = []
        display_order = []

        for tab in all_tabs:
            class_ = tab.__class__.__name__
            if class_ in ["FileEditorTab", "FileViewerTab", "FileTab"]:
                continue

            title = tab.title
            ID = tab.ID
            display_order.append(ID)
            save_, dependencies = tab.save_state()
            tab_saves.append((class_, ID, title, save_, dependencies))

        load_order = sorted(display_order)
        save = {
            "tab_saves": tab_saves,
            "display_order": display_order,
            "load_order": load_order,
        }
        return save

    def restore_state(self, save):
        start_index = self.tab_widget.count()
        if self.ID_counter != 0:
            print("Save files can only be loaded into new kMap windows.")
            return

        tab_saves = save["tab_saves"]
        for ID in save["load_order"]:
            for tab_save in tab_saves:
                if tab_save[1] == ID:
                    self.open_tab_by_save(tab_save)

        tabbar = self.tab_widget.tabBar()
        for i, ID in enumerate(save["display_order"]):
            tab = self.get_tab_by_ID(ID)
            index = self.tab_widget.indexOf(tab)
            tabbar.moveTab(index, i + start_index)

    def _open_tab(self, tab, title, tooltip=None, index=None, ID=None):
        self.ID_counter += 1
        ID = self.ID_counter if ID is None else ID
        tab.set_ID(ID)

        index = self.tab_widget.addTab(tab, title)

        self.tab_widget.setCurrentIndex(index)

        if tooltip is not None:
            self.tab_widget.setTabToolTip(index, tooltip)

        self.tab_added.emit(tab)

    def _connect(self):
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_current_tab)
