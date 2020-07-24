from PyQt5.QtWidgets import QWidget
from map.ui.sliceddatatab_ui import SlicedDataTabUI
from map.library.library import get_ID_from_tab_text
from map.view.matplotlibwindow import MatplotlibWindow


class SlicedDataTab(QWidget, SlicedDataTabUI):

    def __init__(self, model, data):

        super().__init__()

        self.model = model
        self.data = data
        self.displayed = None

        self.setupUi()

        self.change_slice(0)

    def close(self):

        tab_widget = self.parentWidget().parentWidget()

        index = tab_widget.indexOf(self)
        tab_title = tab_widget.tabText(index)
        ID = get_ID_from_tab_text(tab_title)

        try:
            self.model.remove_sliced_by_ID(ID)

        except LookupError:
            log = logging.getLogger('map')
            log.exception('Removing of data with ID %i couldn\'t' % ID +
                          ' be removed. Traceback:')
            log.error('Error occured when trying to remove data. ' +
                      'Correct behaviour from now on can\'t be ' +
                      'guaranteed!')

    def change_slice(self, index):

        self.displayed = self.data.slice_from_idx(index)
        self.plot_item.plot(self.displayed)
        self.update()

    def update(self):

        self.crosshair.update_label(self.plot_item.displayed_plot_data)

    def crosshair_changed(self):

        self.crosshair.update_label(self.plot_item.displayed_plot_data)

    def display_in_matplotlib(self):

        self.window = MatplotlibWindow(self.displayed, self.data.name)
