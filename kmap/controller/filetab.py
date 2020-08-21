# Python Imports
from os.path import abspath

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import QDir

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.config.config import config


class FileTab(Tab):

    def __init__(self, path, richText=False):

        super(FileTab, self).__init__()

        self.path = path
        self.richText = richText

    def reload_text(self):

        with open(self.path, 'r') as file:
            text = file.read()

        self.refresh_display(text)

    def refresh_display(self, text):

        if self.richText:
            self.display.setHtml(text)
        else:
            self.display.setPlainText(text)

    def find_next(self):

        self.display.find(self.line_edit.text())

    def find_prev(self):

        self.display.find(self.line_edit.text(), QTextDocument.FindBackward)

    def _setup(self):

        label = self.title.text()
        self.title.setText(label + self.path)

    def _connect(self):

        self.find_next_button.clicked.connect(self.find_next)
        self.find_prev_button.clicked.connect(self.find_prev)
        self.reload_button.clicked.connect(self.reload_text)


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/fileviewertab.ui')
FileViewerTab_UI, _ = uic.loadUiType(UI_file)


class FileViewerTab(FileTab, FileViewerTab_UI):

    def __init__(self, path, richText=False):

        # Setup GUI
        super(FileViewerTab, self).__init__(path, richText=richText)
        self.setupUi(self)
        self._connect()

        self._setup()
        self.reload_text()


# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/fileeditortab.ui')
FileEditorTab_UI, _ = uic.loadUiType(UI_file)


class FileEditorTab(FileTab, FileEditorTab_UI):

    def __init__(self, path):

        # Setup GUI
        super(FileEditorTab, self).__init__(path, richText=False)
        self.setupUi(self)
        self._connect()

        self._setup()
        self.reload_text()

    def save(self):

        if self.richText:
            text = self.display.toHtml()

        else:
            text = self.display.toPlainText()

        with open(self.path, 'wt') as file:
            file.write(text)

    def _connect(self):

        FileTab._connect(self)

        self.save_button.clicked.connect(self.save)
