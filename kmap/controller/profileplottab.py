# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.orbitaldatatab import OrbitalDataTab

# Load .ui File
UI_file = __directory__ + '/ui/profileplottab.ui'
ProfilePlotTab_UI, _ = uic.loadUiType(UI_file)


class ProfilePlotTab(QWidget, ProfilePlotTab_UI):

    def __init__(self, tab_widget, *args, **kwargs):

        # Setup GUI
        super(ProfilePlotTab, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.sliced_tabs = []
        self.orbital_tabs = []

        self._setup()
        self._connect(tab_widget)

        self.load_tabs(tab_widget)

    def refresh_plot(self):

        pass

    def load_tabs(self, tab_widget):

        all_sliced_tabs = tab_widget.get_tabs_of_type(SlicedDataTab)
        all_orbital_tabs = tab_widget.get_tabs_of_type(OrbitalDataTab)

        for tab in all_sliced_tabs:
            self.add_sliced_tab(tab)

        for tab in all_orbital_tabs:
            self.add_orbital_tab(tab)

    def add_tab(self, tab):

        if type(tab) == SlicedDataTab:
            self.add_sliced_tab(tab)

        elif type(tab) == OrbitalDataTab:
            self.add_orbital_tab(tab)

    def add_sliced_tab(self, tab):

        tab.close_requested.connect(self._remove_tab)
        self.sliced_tab_combobox.addItem(tab.get_title())
        self.sliced_tabs.append(tab)

    def add_orbital_tab(self, tab):

        tab.close_requested.connect(self._remove_tab)
        self.orbital_tab_combobox.addItem(tab.get_title())
        self.orbital_tabs.append(tab)

    def _remove_tab(self):

        tab = self.sender()

        if type(tab) == SlicedDataTab:
            self._remove_sliced_tab(tab)
            removed = True

        elif type(tab) == OrbitalDataTab:
            self._remove_orbital_tab(tab)
            removed = True

        if removed:
            self.refresh_plot()

    def _remove_sliced_tab(self, tab):

        index = self.sliced_tabs.index(tab)
        self.sliced_tabs.remove(tab)
        self.sliced_tab_combobox.removeItem(index)

    def _remove_orbital_tab(self, tab):

        index = self.orbital_tabs.index(tab)
        self.orbital_tabs.remove(tab)
        self.orbital_tab_combobox.removeItem(index)

    def _remove_orbital(self):

        pass

    def switch_type(self):

        # Widgets associated with line-like plotting (e.g. x/y - Line)
        line_widgets = [self.sliced_x_checkbox, self.sliced_y_checkbox,
                        self.orbital_x_checkbox, self.orbital_y_checkbox]
        show_bool = self.line_radiobutton.isChecked()
        for widget in line_widgets:
            widget.blockSignals(True)
            widget.setChecked(False)
            widget.setVisible(show_bool)
            widget.blockSignals(False)

        # Widgets associated with ring-like plotting (e.g. ROI, Annulus)
        circle_widgets = [self.sliced_annulus_checkbox,
                          self.sliced_border_checkbox,
                          self.sliced_roi_checkbox,
                          self.orbital_annulus_checkbox,
                          self.orbital_border_checkbox,
                          self.orbital_roi_checkbox]
        show_bool = self.circle_radiobutton.isChecked()
        for widget in circle_widgets:
            widget.blockSignals(True)
            widget.setChecked(False)
            widget.setVisible(show_bool)
            widget.blockSignals(False)

    def _setup(self):

        self.switch_type()

    def _connect(self, tab_widget):

        tab_widget.tab_added.connect(self.add_tab)

        self.refresh_button.clicked.connect(self.refresh_plot)
        self.circle_radiobutton.toggled.connect(self.switch_type)
