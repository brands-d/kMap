# Python Imports
from os.path import abspath

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtGui import QTextDocument

# Own Imports
from kmap import __directory__
from kmap.library.qwidgetsub import Tab
from kmap.config.config import config


class FileTab(Tab):

    def __init__(self, path, title, richText=False):

        super(FileTab, self).__init__()

        self.title = title
        self.path = path
        self.richText = richText

    @classmethod
    def init_from_save(cls, save):

        path = save['path']
        title = save['title']
        richText = save['richText']

        tab = cls(path, title, richText)

        return tab

    def save_state(self):

        save = {'title': self.title,
                'path': self.path,
                'richText': self.richText}

        return save, []

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

    def get_title(self):

        return self.title

    def set_title(self, title):

        self.title = title

    def _setup(self):

        label = self.title_line_edit.text()
        self.title_line_edit.setText(label + str(self.path))

    def _connect(self):

        self.find_next_button.clicked.connect(self.find_next)
        self.find_prev_button.clicked.connect(self.find_prev)
        self.reload_button.clicked.connect(self.reload_text)


# Load .ui File
UI_file = __directory__ / 'ui/fileviewertab.ui'
FileViewerTab_UI, _ = uic.loadUiType(UI_file)


class FileViewerTab(FileTab, FileViewerTab_UI):

    def __init__(self, path, title, richText=False):
        # Setup GUI
        super(FileViewerTab, self).__init__(path, title, richText=richText)
        self.setupUi(self)
        self._connect()

        self._setup()
        self.reload_text()


# Load .ui File
UI_file = __directory__ / 'ui/fileeditortab.ui'
FileEditorTab_UI, _ = uic.loadUiType(UI_file)


class FileEditorTab(FileTab, FileEditorTab_UI):

    def __init__(self, path, title, *args, **kwargs):

        # Setup GUI
        super(FileEditorTab, self).__init__(path, title, richText=False)
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
