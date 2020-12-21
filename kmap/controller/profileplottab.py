# Python Imports
from itertools import chain

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Third Party Imports
import numpy as np

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.controller.sliceddatatab import SlicedDataTab
from kmap.controller.orbitaldatatab import OrbitalDataTab
from kmap.controller.matplotlibwindow import MatplotlibLineWindow

# Load .ui File
UI_file = __directory__ / 'ui/profileplottab.ui'
ProfilePlotTab_UI, _ = uic.loadUiType(UI_file)


class ProfilePlotTab(Tab, ProfilePlotTab_UI):

    def __init__(self, tab_widget, title, *args, **kwargs):
        # Setup GUI
        super(ProfilePlotTab, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # List of SlicedDataTabs and OrbitalDataTabs this ProfilePlotTab
        # know about
        self.tabs = []
        # For each tab in self.tabs a 6-element long sublist with bools
        # denoted which plots options (checkboxes) are enabled for the
        # corresponding tab
        self.show_options = []
        self.title = title

        self._setup()
        self._connect(tab_widget)

        self.load_tabs(tab_widget)

    def refresh_plot(self):
        is_slice_plot = self.slice_radiobutton.isChecked()
        is_line_plot = self.line_radiobutton.isChecked()
        phi_sample = self.phi_sample_spinbox.value()
        line_sample = self.line_sample_spinbox.value()
        normalized = self.normalize_checkbox.isChecked()
        x_label = 'None'
        self.plot_item.clear()

        if is_slice_plot:
            regions = np.array(['center', 'x', 'y', 'roi', 'border',
                                'ring'])[
                self.show_options[self.tab_combobox.currentIndex()]]

            if self.center_checkbox.isChecked():
                np.insert(regions, 0, 'center')

            if not list(regions):
                return

            for region in regions:
                tab = self.current_tab()
                axis = tab.get_axis()
                data = [tab.get_data(), axis]
                crosshair = tab.get_crosshair().model
                title = tab.get_title()
                self.plot_item.plot(data, title, crosshair,
                                    region=region,
                                    phi_sample=phi_sample,
                                    line_sample=line_sample,
                                    normalized=normalized)
                axis = tab.get_data().axes[axis]
                x_label = '%s [%s]' % (axis.label, axis.units)

        else:
            for tab, show_options in zip(self.tabs, self.show_options):
                data = tab.get_displayed_plot_data()
                bottom_label, left_label = tab.get_plot_labels()
                crosshair = tab.get_crosshair().model
                title = tab.get_title()
                x_label = ''

                if is_line_plot and show_options[1]:
                    self.plot_item.plot(data, title, crosshair,
                                        region='x',
                                        phi_sample=phi_sample,
                                        line_sample=line_sample,
                                        normalized=normalized)
                    x_label = left_label

                if is_line_plot and show_options[2]:
                    self.plot_item.plot(data, title, crosshair,
                                        region='y',
                                        phi_sample=phi_sample,
                                        line_sample=line_sample,
                                        normalized=normalized)
                    x_label = bottom_label

                if not is_line_plot and show_options[3]:
                    self.plot_item.plot(data, title, crosshair,
                                        region='roi',
                                        phi_sample=phi_sample,
                                        line_sample=line_sample,
                                        normalized=normalized)
                    x_label = 'Angle Phi [°]'

                if not is_line_plot and show_options[4]:
                    self.plot_item.plot(data, title, crosshair,
                                        region='border',
                                        phi_sample=phi_sample,
                                        line_sample=line_sample,
                                        normalized=normalized)
                    x_label = 'Angle Phi [°]'

                if not is_line_plot and show_options[5]:
                    self.plot_item.plot(data, title, crosshair,
                                        region='ring',
                                        phi_sample=phi_sample,
                                        line_sample=line_sample,
                                        normalized=normalized)
                    x_label = 'Angle Phi [°]'

        self.plot_item.set_label(x_label, 'Intensity [a.u.]')

    def save_state(self):
        if self.circle_radiobutton.isChecked():
            type_ = 'circle'

        elif self.line_radiobutton.isChecked():
            type_ = 'line'

        else:
            type_ = 'slice'

        states = []
        checkboxes = [self.center_checkbox, self.x_checkbox,
                      self.y_checkbox, self.roi_checkbox,
                      self.border_checkbox, self.annulus_checkbox]
        for checkbox in checkboxes:
            states.append(checkbox.checkState())

        sample_rate = [self.phi_sample_spinbox.value(),
                       self.line_sample_spinbox.value()]

        save = {'title': self.get_title(),
                'type': type_,
                'tab_index': self.tab_combobox.currentIndex(),
                'states': states,
                'sample_rate': sample_rate}

        return save, []

    def restore_state(self, save):
        type_ = save['type']

        if type_ == 'circle':
            self.circle_radiobutton.click()

        elif type_ == 'line':
            self.line_radiobutton.click()

        elif type_ == 'slice':
            self.slice_radiobutton.click()

        else:
            raise ValueError

        tab_index = save['tab_index']
        self.tab_combobox.setCurrentIndex(tab_index)

        sample_rate = save['sample_rate']
        self.phi_sample_spinbox.setValue(sample_rate[0])
        self.line_sample_spinbox.setValue(sample_rate[1])

        checkboxes = [self.center_checkbox, self.x_checkbox,
                      self.y_checkbox, self.roi_checkbox,
                      self.border_checkbox, self.annulus_checkbox]
        for state, checkbox in zip(save['states'], checkboxes):
            checkbox.setCheckState(state)

        self.refresh_button.click()

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
            self.show_options.append(6 * [False])

    def export_to_txt(self):
        data = self.plot_item.get_data()

        text = ''

        for data_set in data:
            name = data_set['name']
            x = data_set['x']
            y = data_set['y']
            text += '# ' + name + '\n'
            for xi, yi in zip(x, y):
                text += '%g  %g \n' % (xi, yi)
            text += '\n'

        return text

    def display_in_matplotlib(self):
        data = self.plot_item.get_data()

        window = MatplotlibLineWindow(data)

        return window

    def current_tab(self):
        return self.tabs[self.tab_combobox.currentIndex()]

    def _remove_tab(self):
        tab = self.sender()

        if tab in self.tabs:
            index = self.tabs.index(tab)
            self.tab_combobox.removeItem(index)
            del self.tabs[index]
            del self.show_options[index]

            self.refresh_plot()

    def rename_loaded_tab(self, tab, new_name):
        try:
            index = self.tabs.index(tab)
            self.tab_combobox.setItemText(index, new_name)

        except ValueError:
            pass

    def switch_type(self):
        # Widgets associated with line-like plotting (e.g. x/y - Line)
        line_widgets = [self.x_checkbox, self.y_checkbox]
        # Widgets associated with ring-like plotting (e.g. ROI, Annulus)
        circle_widgets = [self.annulus_checkbox,
                          self.border_checkbox, self.roi_checkbox]

        show_slice_bool = self.slice_radiobutton.isChecked()
        show_line_bool = True if self.line_radiobutton.isChecked(
        ) or show_slice_bool else False
        show_circle_bool = True if self.circle_radiobutton.isChecked(
        ) or show_slice_bool else False

        for widget in chain(line_widgets, circle_widgets):
            widget.blockSignals(True)

            if widget in line_widgets:
                widget.setVisible(show_line_bool)

            if widget in circle_widgets:
                widget.setVisible(show_circle_bool)

            widget.blockSignals(False)

        self.center_checkbox.setVisible(show_slice_bool)

        other_widgets = [self.phi_sample_label, self.phi_sample_spinbox,
                         self.line_sample_label, self.line_sample_spinbox]

        for widget in other_widgets:
            widget.setVisible(not show_slice_bool)

    def _change_tab(self, index):
        if isinstance(self.tabs[index], SlicedDataTab):
            self.slice_radiobutton.setVisible(True)

        else:
            self.slice_radiobutton.setVisible(False)

            if self.slice_radiobutton.isChecked():
                self.line_radiobutton.setChecked(True)

        checkboxes = [self.center_checkbox,
                      self.x_checkbox, self.y_checkbox,
                      self.roi_checkbox, self.border_checkbox,
                      self.annulus_checkbox]

        for checkbox, show in zip(checkboxes, self.show_options[index]):
            checkbox.blockSignals(True)
            checkbox.setChecked(show)
            checkbox.blockSignals(False)

    def _change_checkbox(self):
        checkbox = self.sender()
        checkboxes = [self.center_checkbox,
                      self.x_checkbox, self.y_checkbox,
                      self.roi_checkbox, self.border_checkbox,
                      self.annulus_checkbox]

        tab_index = self.tab_combobox.currentIndex()
        if tab_index != -1:
            checkbox_index = checkboxes.index(checkbox)
            self.show_options[tab_index][checkbox_index] = checkbox.isChecked()

    def _setup(self):
        self.switch_type()

    def _connect(self, tab_widget):
        tab_widget.tab_added.connect(self.add_tab)

        self.refresh_button.clicked.connect(self.refresh_plot)
        self.circle_radiobutton.toggled.connect(self.switch_type)
        self.slice_radiobutton.toggled.connect(self.switch_type)

        self.tab_combobox.currentIndexChanged.connect(self._change_tab)
        self.center_checkbox.stateChanged.connect(self._change_checkbox)
        self.x_checkbox.stateChanged.connect(self._change_checkbox)
        self.y_checkbox.stateChanged.connect(self._change_checkbox)
        self.roi_checkbox.stateChanged.connect(self._change_checkbox)
        self.border_checkbox.stateChanged.connect(self._change_checkbox)
        self.annulus_checkbox.stateChanged.connect(self._change_checkbox)
