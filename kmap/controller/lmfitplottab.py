# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab

# Load .ui File
UI_file = __directory__ + '/ui/lmfitplottab.ui'
LMFitPlotTab_UI, _ = uic.loadUiType(UI_file)


class LMFitPlotTab(Tab, LMFitPlotTab_UI):

    def __init__(self, results, orbitals, axis, *args, **kwargs):

        self.results = results
        self.orbitals = orbitals
        self.x_axis = axis

        # Setup GUI
        super(LMFitPlotTab, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._connect()

        self.refresh_plot()

    def export_to_txt(self):

        data = self.plot_item.get_data()

        text = 'name,x,y\n'

        for data_set in data:
            text += '{name},{x},{y}\n'.format(**data_set)              

        return text
        
    def refresh_plot(self):

        possible_params = ['w_', 'phi_', 'theta_', 'psi_']
        possible_labels = ['Weight [1]', 'Phi [°]', 'Theta [°]', 'Psi [°]']
        param = possible_params[self.parameter_combobox.currentIndex()]

        self.plot_item.clear()

        for orbital in self.orbitals:
            y = [result.params[param + str(orbital.ID)]
                 for result in self.results]
            x = self.x_axis.axis
            title = orbital.name

            self.plot_item.plot(x, y, title)

        self.plot_item.set_label('%s [%s]' % (self.x_axis.label,
                                              self.x_axis.units),
                                 possible_labels[self.parameter_combobox.currentIndex()])

    def _connect(self):

        self.refresh_button.clicked.connect(self.refresh_plot)
