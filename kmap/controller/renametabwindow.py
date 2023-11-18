from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow

from kmap.ui.renametabwindow import Ui_rename_tab as RenameTabWindow_UI


class RenameTabWindow(QMainWindow, RenameTabWindow_UI):
    title_chosen = Signal(str)

    def __init__(self, *args, **kwargs):
        self.new_title = None

        # Setup GUI
        super(RenameTabWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self._connect()

        self.show()

    def name_chosen(self):
        self.new_title = self.rename_tab_edit.text()

        self.close()

    def closeEvent(self, event):
        self.title_chosen.emit(self.new_title)
        self.deleteLater()
        event.accept()

    def _setup(self):
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    def _connect(self):
        self.rename_tab_edit.returnPressed.connect(self.name_chosen)
