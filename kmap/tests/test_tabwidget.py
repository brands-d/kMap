import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtTest import QTest as qt
from kmap.model.model import Model
from kmap import kMap
from kmap.view.mainwindow import MainWindow


class TestMainWindow(unittest.TestCase):

    app = kMap.kMap([])

    def setUp(self):

        self.model = Model(TestMainWindow.app)
        self.window = MainWindow(self.model)

    def test_default_state(self):

        self.assertEqual(self.window.tab_widget.count(), 1)

    '''UNDER CONSTRUCTION
    def test_default_state(self):

        qt.keySequence(self.window, QKeySequence('Ctrl+f'))'''
