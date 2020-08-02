from os.path import abspath
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QTextDocument
from kmap.ui.filetab_ui import FileViewerTabUI, FileEditorTabUI
from kmap.model.filetab_model import FileViewerTabModel, FileEditorTabModel
from kmap import __directory__


class FileViewerTab(FileViewerTabUI):

    def __init__(self, path, richText=False):

        self.path = path
        self.richText = richText
        self._set_model()

        FileViewerTabUI.__init__(self)

        self.reload_text()
        self.refresh_display()

    def reload_text(self):

        self.model.read_file(self.path)

    def refresh_display(self):

        text = self.model.text

        if self.richText:
            self.display.setHtml(text)
        else:
            self.display.setPlainText(text)

    def find_next(self):

        self.display.find(self.line_edit.text())

    def find_prev(self):

        self.display.find(self.line_edit.text(), QTextDocument.FindBackward)

    def _set_model(self):

        self.model = FileViewerTabModel()


class FileEditorTab(FileViewerTab, FileEditorTabUI):

    def __init__(self, path):

        super().__init__(path, richText=False)

    def _set_model(self):

        self.model = FileEditorTabModel()

    def save(self):

        text = self.display.toPlainText()
        self.model.save_file(text, self.path)
