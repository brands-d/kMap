# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.controller.matplotlibwindow import MatplotlibLineWindow

# Load .ui File
UI_file = __directory__ / 'ui/lmfitplottab.ui'
LMFitPlotTab_UI, _ = uic.loadUiType(UI_file)


class LMFitPlotTab(Tab, LMFitPlotTab_UI):

    def __init__(self, results, orbitals, axis, residuals, result_tab, *args,
                 **kwargs):
        self.results = results
        self.result_tab = result_tab
        self.orbitals = orbitals
        self.x_axis = axis
        self.residuals = residuals

        # Setup GUI
        super(LMFitPlotTab, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._connect()

        self.refresh_plot()

    @classmethod
    def init_from_save(cls, save, tab):
        results = save['results']
        axis = save['axis']
        residuals = save['residuals'] if 'residuals' in save else None
        orbitals = tab.get_orbitals()

        tab = LMFitPlotTab(results, orbitals, axis, residuals, tab)

        return tab

    def save_state(self):
        save = {'title': self.title,
                'results': self.results,
                'axis': self.x_axis,
                'residuals': self.residuals}

        return save, [self.result_tab]

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

    def refresh_plot(self):
        x = self.x_axis.axis
        x_label = '%s [%s]' % (self.x_axis.label, self.x_axis.units)
        self.plot_item.clear()

        if self.parameter_combobox.currentText() == 'Residual':
            title = 'Residual'
            y = self.residuals
            self.plot_item.plot(x, y, title)
            y_label = '|Residual|'

        else:
            possible_params = ['w_', 'phi_', 'theta_', 'psi_']
            possible_labels = ['Weight [1]', 'Phi [°]', 'Theta [°]', 'Psi [°]']
            param = possible_params[self.parameter_combobox.currentIndex()]

            for orbital in self.orbitals:
                y = [result.params[param + str(orbital.ID)]
                     for result in self.results]
                title = orbital.name

                self.plot_item.plot(x, y, title)

            y_label = possible_labels[self.parameter_combobox.currentIndex()]

        self.plot_item.set_label(x_label, y_label)

    def display_in_matplotlib(self):
        data = self.plot_item.get_data()

        window = MatplotlibLineWindow(data)

        return window

    def _connect(self):
        self.refresh_button.clicked.connect(self.refresh_plot)
