from PyQt5.QtWidgets import QWidget
from kmap.ui.sliceddatatab_ui import SlicedDataTabUI
from kmap.library.misc import get_ID_from_tab_text
from kmap.model.sliceddatatab_model import SlicedDataTabModel
from kmap.controller.matplotlibwindow import MatplotlibWindow


class SlicedDataTab(SlicedDataTabUI):

    def __init__(self, path):

        self.model = SlicedDataTabModel(path)

        SlicedDataTabUI.__init__(self)

        self.change_slice(0, 0)

    def get_title(self):

        data = self.model.data

        if data:
            id_ = data.ID

            if 'alias' in data.meta_data:
                text = data.meta_data['alias']
            else:
                text = data.name

            title = '%s (%i)' % (text, id_)

        else:
            title = 'NO DATA'

        return title

    def change_slice(self, index, axis):

        data = self.model.change_slice(index, axis)

        self.plot_item.plot(data)
        # self.update()

    def crosshair_changed(self):

        data = self.model.displayed_plot_data
        self.crosshair.update_label()

    def display_in_matplotlib(self):

        data = self.model.displayed_plot_data
        title = self.get_title()

        self.window = MatplotlibWindow(data, title)
