from PyQt5.QtWidgets import QWidget
from kmap.config.config import config


class FixedAspectWidget(QWidget):

    def __init__(self):

        super().__init__()

    def heightForWidth(self, width, ratio):

        return int(width / ratio)

    def widthForHeight(self, height, ratio):

        return int(height * ratio)

    def resizeEvent(self, event):
        '''BUG: For unknown reasons the resizeEvent is called multiple
        times with outdated sizes, thus if the user lowers the side that
        is too large, it will not update correctly.'''
        event.ignore()

        ratio = float(config.get_key('matplotlib', 'forced_aspect_ratio'))
        if ratio == 0:
            return

        old_width = event.oldSize().width()
        old_height = event.oldSize().height()
        new_width = event.size().width()
        new_height = event.size().height()

        if old_width == new_width:
            if old_height == new_height:
                # No change
                return

            else:
                # Only height changed -> use height
                height = new_height
                width = self.widthForHeight(height, ratio)

        else:
            if old_height == new_height:
                # Only width changed -> use width
                width = new_width
                height = self.heightForWidth(width, ratio)

            else:
                # Both changed -> use larger one
                if new_width >= new_height:
                    # Width is larger
                    width = new_width
                    height = self.heightForWidth(width, ratio)

                else:
                    # Height is larger
                    height = new_height
                    width = self.widthForHeight(height, ratio)

        self.blockSignals(True)
        self.resize(width, height)
        self.blockSignals(False)
