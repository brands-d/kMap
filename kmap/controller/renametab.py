# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDir

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ + \
    QDir.toNativeSeparators('/ui/renametab.ui')
RenameTab_UI, _ = uic.loadUiType(UI_file)


class RenameTab(QWidget, RenameTab_UI):

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(RenameTab, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()
        self.show()
#        self.rename_tab_edit.returnPressed.connect(self._test)

#    def _test(self):
#        self.new_title = self.rename_tab_edit.text()
#        print('pressed:',self.new_title)
#        self.close()

    def _setup(self):

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
