from PyQt5.QtWidgets import QWidget


class AspectWidget(QWidget):

    def __init__(self, ratio):

        self.ratio = ratio

        super().__init__()

    def heightForWidth(self, width):

        return int(width / self.ratio)

    def widthForHeight(self, height):

        return int(height * self.ratio)

    def resizeEvent(self, event):
        '''BUG: For unknown reasons the resizeEvent is called multiple
        times with outdated sizes, thus if the user lowers the side that
        is too large, it will not update correctly.'''
        event.ignore()

        if self.ratio == 0:
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
                width = self.widthForHeight(height)

        else:
            if old_height == new_height:
                # Only width changed -> use width
                width = new_width
                height = self.heightForWidth(width)

            else:
                # Both changed -> use larger one
                if new_width >= new_height:
                    # Width is larger
                    width = new_width
                    height = self.heightForWidth(width)

                else:
                    # Height is larger
                    height = new_height
                    width = self.widthForHeight(height)

        self.blockSignals(True)
        self.resize(width, height)
        self.blockSignals(False)
