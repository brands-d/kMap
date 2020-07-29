from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QPushButton
from kmap.ui.fileviewertab_ui import FileViewerTabUI


class FileEditorTabUI(FileViewerTabUI):

    def _initialize_content(self):

        super()._initialize_content()

        self.display.setReadOnly(False)

        self.save_button = QPushButton('Save (Ctrl + s)')
        self.save_button.setShortcut(QKeySequence('Ctrl+s'))
        self.title_layout.addWidget(self.save_button)

    def _initialize_connections(self):

        super()._initialize_connections()

        # Search
        self.save_button.clicked.connect(self.save)
