# Python Imports
from itertools import chain

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

        # List of SlicedDataTabs and OrbitalDataTabs this ProfilePlotTab
        # know about
        self.tabs = []
        # For each tab in self.tabs a 5-element long sublist with bools
        # denoted which plots options (checkboxes) are enabled for the
        # corresponding tab
        self.show_options = []

        self._setup()
        self._connect(tab_widget)

        self.load_tabs(tab_widget)

    def refresh_plot(self):

        is_line_plot = self.line_radiobutton.isChecked()
        phi_sample = self.phi_sample_spinbox.value()
        line_sample = self.line_sample_spinbox.value()

        self.plot_item.clear()

        for tab, show_options in zip(self.tabs, self.show_options):
            data = tab.get_displayed_plot_data()
            crosshair = tab.get_crosshair().model
            title = tab.get_title()
            
            if is_line_plot and show_options[0]:
                self.plot_item.plot(data, title, crosshair, region='x',
                                    phi_sample=phi_sample,
                                    line_sample=line_sample)

            if is_line_plot and show_options[1]:
                self.plot_item.plot(data, title, crosshair, region='y',
                                    phi_sample=phi_sample,
                                    line_sample=line_sample)

            if not is_line_plot and show_options[2]:
                self.plot_item.plot(data, title, crosshair, region='roi',
                                    phi_sample=phi_sample,
                                    line_sample=line_sample)

            if not is_line_plot and show_options[3]:
                self.plot_item.plot(data, title, crosshair, region='border',
                                    phi_sample=phi_sample,
                                    line_sample=line_sample)

            if not is_line_plot and show_options[4]:
                self.plot_item.plot(data, title, crosshair, region='ring',
                                    phi_sample=phi_sample,
                                    line_sample=line_sample)

    def load_tabs(self, tab_widget):

        for tab in tab_widget.get_tabs_of_type(None):
            self.add_tab(tab)

    def add_tab(self, tab):

        if type(tab) in [SlicedDataTab, OrbitalDataTab]:
            tab.close_requested.connect(self._remove_tab)
            self.tab_combobox.blockSignals(True)
            self.tab_combobox.addItem(tab.get_title())
            self.tab_combobox.blockSignals(False)
            self.tabs.append(tab)
            self.show_options.append(5 * [False])

    def _remove_tab(self):

        tab = self.sender()

        if tab in self.tabs:
            index = self.tabs.index(tab)
            self.tab_combobox.removeItem(index)
            del self.tabs[index]
            del self.show_options[index]

            self.refresh_plot()

    def switch_type(self):

        # Widgets associated with line-like plotting (e.g. x/y - Line)
        line_widgets = [self.x_checkbox, self.y_checkbox]
        # Widgets associated with ring-like plotting (e.g. ROI, Annulus)
        circle_widgets = [self.annulus_checkbox,
                          self.border_checkbox, self.roi_checkbox]

        show_line_bool = self.line_radiobutton.isChecked()

        for widget in chain(line_widgets, circle_widgets):
            widget.blockSignals(True)

            if widget in line_widgets:
                widget.setVisible(show_line_bool)

            else:
                widget.setVisible(not show_line_bool)

            widget.blockSignals(False)

        if show_line_bool:
            x_label = ['Axis', 'a.u.']

        else:
            x_label = ['Angle Phi', '°']

        self.plot_item.set_label(x_label, ['Intensity', 'a.u.'])

    def _change_tab(self, index):

        checkboxes = [self.x_checkbox, self.y_checkbox,
                      self.roi_checkbox, self.border_checkbox,
                      self.annulus_checkbox]

        for checkbox, show in zip(checkboxes, self.show_options[index]):
            checkbox.blockSignals(True)
            checkbox.setChecked(show)
            checkbox.blockSignals(False)

    def _change_checkbox(self):

        checkbox = self.sender()
        checkboxes = [self.x_checkbox, self.y_checkbox,
                      self.roi_checkbox, self.border_checkbox,
                      self.annulus_checkbox]

        tab_index = self.tab_combobox.currentIndex()
        checkbox_index = checkboxes.index(checkbox)

        self.show_options[tab_index][checkbox_index] = checkbox.isChecked()

    def _setup(self):

        self.switch_type()

    def _connect(self, tab_widget):

        tab_widget.tab_added.connect(self.add_tab)

        self.refresh_button.clicked.connect(self.refresh_plot)
        self.circle_radiobutton.toggled.connect(self.switch_type)

        self.tab_combobox.currentIndexChanged.connect(self._change_tab)
        self.x_checkbox.stateChanged.connect(self._change_checkbox)
        self.y_checkbox.stateChanged.connect(self._change_checkbox)
        self.roi_checkbox.stateChanged.connect(self._change_checkbox)
        self.border_checkbox.stateChanged.connect(self._change_checkbox)
        self.annulus_checkbox.stateChanged.connect(self._change_checkbox)
