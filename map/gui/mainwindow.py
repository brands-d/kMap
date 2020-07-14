from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.resize(330, 417)
        self.show()