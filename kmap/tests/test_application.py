import unittest
from PyQt5.QtWidgets import QApplication
from kmap import kMap


class TestMainWindow(unittest.TestCase):

    app = kMap.kMap([])

    def test_default_state(self):

        self.app.test()
