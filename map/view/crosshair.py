from PyQt5.QtWidgets import QGroupBox
from map.ui.crosshair_ui import (
    CrosshairUI, CrosshairROIUI, CrosshairAnnulusUI)
from map.model.crosshair import Crosshair as CM
from map.model.crosshair import CrosshairWithROI as CRM
from map.model.crosshair import CrosshairWithAnnulus as CAM


class Crosshair(QGroupBox, CrosshairUI):

    def __init__(self):

        super().__init__()

        self.setupUi()

        self.set_crosshair_model()

    def set_crosshair_model(self):

        self.crosshair = CM()


class CrosshairROI(Crosshair, CrosshairROIUI):

    def set_crosshair_model(self):

        self.crosshair = CRM()


class CrosshairAnnulus(CrosshairROI, CrosshairAnnulusUI):

    def set_crosshair_model(self):

        self.crosshair = CAM()
