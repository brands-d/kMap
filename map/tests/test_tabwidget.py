import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtTest import QTest as qt
from map.model.model import Model
from map import Map
from map.view.mainwindow import MainWindow


class TestMainWindow(unittest.TestCase):

    app = Map.Map([])

    def setUp(self):

        self.model = Model(TestMainWindow.app)
        self.window = MainWindow(self.model)

    def test_default_state(self):

        self.assertEqual(self.window.tab_widget.count(), 1)

    '''UNDER CONSTRUCTION
    def test_default_state(self):

        qt.keySequence(self.window, QKeySequence('Ctrl+f'))'''
