# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crosshair.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_crosshair(object):
    def setupUi(self, crosshair):
        if not crosshair.objectName():
            crosshair.setObjectName(u"crosshair")
        crosshair.resize(531, 147)
        font = QFont()
        font.setBold(True)
        crosshair.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(crosshair)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupbox = QGroupBox(crosshair)
        self.groupbox.setObjectName(u"groupbox")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        self.groupbox.setFont(font1)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout(self.groupbox)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.enable_label = QLabel(self.groupbox)
        self.enable_label.setObjectName(u"enable_label")
        font2 = QFont()
        font2.setBold(False)
        font2.setItalic(False)
        self.enable_label.setFont(font2)

        self.top_layout.addWidget(self.enable_label)

        self.enable_crosshair_checkbox = QCheckBox(self.groupbox)
        self.enable_crosshair_checkbox.setObjectName(u"enable_crosshair_checkbox")
        self.enable_crosshair_checkbox.setFont(font2)

        self.top_layout.addWidget(self.enable_crosshair_checkbox)

        self.color_label = QLabel(self.groupbox)
        self.color_label.setObjectName(u"color_label")
        font3 = QFont()
        font3.setBold(False)
        self.color_label.setFont(font3)

        self.top_layout.addWidget(self.color_label)

        self.color_combobox = QComboBox(self.groupbox)
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.addItem("")
        self.color_combobox.setObjectName(u"color_combobox")
        self.color_combobox.setFont(font3)
        self.color_combobox.setMaxVisibleItems(8)
        self.color_combobox.setMaxCount(8)

        self.top_layout.addWidget(self.color_combobox)


        self.layout.addLayout(self.top_layout)

        self.bottom_layout = QGridLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.point_value = QLabel(self.groupbox)
        self.point_value.setObjectName(u"point_value")
        self.point_value.setFont(font3)
        self.point_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.point_value, 1, 3, 1, 1)

        self.y_label = QLabel(self.groupbox)
        self.y_label.setObjectName(u"y_label")
        self.y_label.setFont(font3)
        self.y_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.y_label, 1, 0, 1, 1)

        self.y_spinbox = QDoubleSpinBox(self.groupbox)
        self.y_spinbox.setObjectName(u"y_spinbox")
        self.y_spinbox.setFont(font3)
        self.y_spinbox.setAlignment(Qt.AlignCenter)
        self.y_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.y_spinbox.setKeyboardTracking(False)
        self.y_spinbox.setMinimum(-100.000000000000000)
        self.y_spinbox.setMaximum(100.000000000000000)
        self.y_spinbox.setSingleStep(0.020000000000000)

        self.bottom_layout.addWidget(self.y_spinbox, 1, 1, 1, 1)

        self.point_label = QLabel(self.groupbox)
        self.point_label.setObjectName(u"point_label")
        self.point_label.setFont(font3)
        self.point_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.point_label, 1, 2, 1, 1)

        self.x_label = QLabel(self.groupbox)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setFont(font3)
        self.x_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.x_label, 0, 0, 1, 1)

        self.distance_value = QLabel(self.groupbox)
        self.distance_value.setObjectName(u"distance_value")
        self.distance_value.setFont(font3)
        self.distance_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.distance_value, 0, 3, 1, 1)

        self.x_spinbox = QDoubleSpinBox(self.groupbox)
        self.x_spinbox.setObjectName(u"x_spinbox")
        self.x_spinbox.setFont(font3)
        self.x_spinbox.setAlignment(Qt.AlignCenter)
        self.x_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.x_spinbox.setKeyboardTracking(False)
        self.x_spinbox.setMinimum(-100.000000000000000)
        self.x_spinbox.setMaximum(100.000000000000000)
        self.x_spinbox.setSingleStep(0.020000000000000)

        self.bottom_layout.addWidget(self.x_spinbox, 0, 1, 1, 1)

        self.distance_label = QLabel(self.groupbox)
        self.distance_label.setObjectName(u"distance_label")
        self.distance_label.setFont(font3)
        self.distance_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.distance_label, 0, 2, 1, 1)

        self.total_area_label = QLabel(self.groupbox)
        self.total_area_label.setObjectName(u"total_area_label")
        self.total_area_label.setFont(font3)
        self.total_area_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.total_area_label, 0, 4, 1, 1)

        self.total_area_value = QLabel(self.groupbox)
        self.total_area_value.setObjectName(u"total_area_value")
        self.total_area_value.setFont(font3)
        self.total_area_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.total_area_value, 0, 5, 1, 1)


        self.layout.addLayout(self.bottom_layout)


        self.horizontalLayout_2.addWidget(self.groupbox)


        self.retranslateUi(crosshair)

        QMetaObject.connectSlotsByName(crosshair)
    # setupUi

    def retranslateUi(self, crosshair):
        crosshair.setWindowTitle(QCoreApplication.translate("crosshair", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("crosshair", u"Crosshair", None))
        self.enable_label.setText(QCoreApplication.translate("crosshair", u"Enable:", None))
        self.enable_crosshair_checkbox.setText(QCoreApplication.translate("crosshair", u"Crosshair", None))
        self.color_label.setText(QCoreApplication.translate("crosshair", u"Color:", None))
        self.color_combobox.setItemText(0, QCoreApplication.translate("crosshair", u"black", None))
        self.color_combobox.setItemText(1, QCoreApplication.translate("crosshair", u"white", None))
        self.color_combobox.setItemText(2, QCoreApplication.translate("crosshair", u"red", None))
        self.color_combobox.setItemText(3, QCoreApplication.translate("crosshair", u"blue", None))
        self.color_combobox.setItemText(4, QCoreApplication.translate("crosshair", u"green", None))
        self.color_combobox.setItemText(5, QCoreApplication.translate("crosshair", u"cyan", None))
        self.color_combobox.setItemText(6, QCoreApplication.translate("crosshair", u"magenta", None))
        self.color_combobox.setItemText(7, QCoreApplication.translate("crosshair", u"yellow", None))

        self.point_value.setText("")
        self.y_label.setText(QCoreApplication.translate("crosshair", u"y-Pos.", None))
#if QT_CONFIG(tooltip)
        self.point_label.setToolTip(QCoreApplication.translate("crosshair", u"Intensity at the crosshair.", None))
#endif // QT_CONFIG(tooltip)
        self.point_label.setText(QCoreApplication.translate("crosshair", u"Int. (Point)", None))
        self.x_label.setText(QCoreApplication.translate("crosshair", u"x-Pos.", None))
        self.distance_value.setText("")
#if QT_CONFIG(tooltip)
        self.distance_label.setToolTip(QCoreApplication.translate("crosshair", u"Distance of the crosshair from the origin.", None))
#endif // QT_CONFIG(tooltip)
        self.distance_label.setText(QCoreApplication.translate("crosshair", u"<html><head/><body><p>k<span style=\"vertical-align:sub;\">||</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.total_area_label.setToolTip(QCoreApplication.translate("crosshair", u"Total area (only non-NaN).", None))
#endif // QT_CONFIG(tooltip)
        self.total_area_label.setText(QCoreApplication.translate("crosshair", u"Area (Total)", None))
        self.total_area_value.setText("")
    # retranslateUi

