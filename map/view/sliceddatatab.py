from map.ui.sliceddatatab_ui import SlicedDataTabUI
from PyQt5.QtWidgets import QWidget
from map.library.library import get_ID_from_tab_text

class SlicedDataTab(QWidget, SlicedDataTabUI):

    def __init__(self, model, data):

        super().__init__()

        self.model = model
        
        self.setupUi()

        self.plot_item.plot(data.slice_from_idx(0))

    def close(self):

        tab_widget = self.parentWidget().parentWidget()

        index = tab_widget.indexOf(self)
        tab_title = tab_widget.tabText(index)
        ID = get_ID_from_tab_text(tab_title)

        try:
            self.model.remove_sliced_by_ID(ID)

        except LookupError:
            log = logging.getLogger('root')
            log.exception('Removing of data with ID %i couldn\'t' % ID +
                          ' be removed. Traceback:')
            log.error('Error occured when trying to remove data. ' +
                      'Correct behaviour from now on can\'t be ' +
                      'guaranteed!')