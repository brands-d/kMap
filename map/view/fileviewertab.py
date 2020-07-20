from map.ui.fileviewertab_ui import FileViewerTabUI
from os.path import abspath
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QTextDocument


class FileViewerTab(QWidget, FileViewerTabUI):

    def __init__(self, file_path, richText=False):

        super().__init__()

        self.file_path = abspath(file_path)
        self.richText = richText

        self.setupUi()

        self.open_file()

    def open_file(self):

        with open(self.file_path, 'r') as f:
            if self.richText:
                self.display.setMarkdown(f.read())

            else:
                self.display.setPlainText(f.read())

    def close(self):
        pass

    def find_next(self):

        self.display.find(self.line_edit.text())

    def find_prev(self):

        self.display.find(self.line_edit.text(), QTextDocument.FindBackward)
