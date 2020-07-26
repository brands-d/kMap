import logging
from PyQt5.QtWidgets import QWidget
from map.library.library import get_ID_from_tab_text
from map.ui.orbitaldatatab_ui import OrbitalDataTabUI


class OrbitalDataTab(QWidget, OrbitalDataTabUI):

    def __init__(self, model, orbital):

        super().__init__()

        self.model = model
        self.displayed = None

        self.setupUi()

        self.displayed = orbital.get_kmap(E_kin=50, phi=10, Ak_type='toroid')
        self.plot_item.plot(self.displayed)

    def close(self):

        tab_widget = self.parentWidget().parentWidget()

        index = tab_widget.indexOf(self)
        tab_title = tab_widget.tabText(index)
        ID = get_ID_from_tab_text(tab_title)

        try:
            self.model.remove_orbital_by_ID(ID)

        except LookupError:
            log = logging.getLogger('map')
            log.exception('Removing of data with ID %i couldn\'t' % ID +
                          ' be removed. Traceback:')
            log.error('Error occured when trying to remove data. ' +
                      'Correct behaviour from now on can\'t be ' +
                      'guaranteed!')

    def crosshair_changed(self):

        self.crosshair.update_label(self.plot_item.displayed_plot_data)