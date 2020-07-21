from map.view.fileviewertab import FileViewerTab
from map.ui.fileeditortab_ui import FileEditorTabUI


class FileEditorTab(FileViewerTab, FileEditorTabUI):

    def __init__(self, file_path):

        super().__init__(file_path, richText=False)

    def save(self):

        with open(self.file_path, 'wt') as f:
            f.write(self.display.toPlainText())
