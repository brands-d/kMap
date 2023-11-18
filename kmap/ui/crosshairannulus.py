# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crosshairannulus.ui'
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
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_crosshairannulus(object):
    def setupUi(self, crosshairannulus):
        if not crosshairannulus.objectName():
            crosshairannulus.setObjectName(u"crosshairannulus")
        crosshairannulus.resize(690, 231)
        self.horizontalLayout = QHBoxLayout(crosshairannulus)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupbox = QGroupBox(crosshairannulus)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout(self.groupbox)
        self.layout.setSpacing(3)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(5, 15, 5, 0)
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.enable_label = QLabel(self.groupbox)
        self.enable_label.setObjectName(u"enable_label")
        font1 = QFont()
        font1.setBold(False)
        font1.setItalic(False)
        self.enable_label.setFont(font1)

        self.top_layout.addWidget(self.enable_label)

        self.enable_crosshair_checkbox = QCheckBox(self.groupbox)
        self.enable_crosshair_checkbox.setObjectName(u"enable_crosshair_checkbox")
        self.enable_crosshair_checkbox.setFont(font1)

        self.top_layout.addWidget(self.enable_crosshair_checkbox)

        self.enable_roi_checkbox = QCheckBox(self.groupbox)
        self.enable_roi_checkbox.setObjectName(u"enable_roi_checkbox")
        font2 = QFont()
        font2.setBold(False)
        self.enable_roi_checkbox.setFont(font2)

        self.top_layout.addWidget(self.enable_roi_checkbox)

        self.enable_annulus_checkbox = QCheckBox(self.groupbox)
        self.enable_annulus_checkbox.setObjectName(u"enable_annulus_checkbox")
        self.enable_annulus_checkbox.setFont(font2)

        self.top_layout.addWidget(self.enable_annulus_checkbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.top_layout.addItem(self.horizontalSpacer)

        self.color_label = QLabel(self.groupbox)
        self.color_label.setObjectName(u"color_label")
        self.color_label.setFont(font2)

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
        self.color_combobox.setFont(font2)
        self.color_combobox.setMaxVisibleItems(8)
        self.color_combobox.setMaxCount(8)

        self.top_layout.addWidget(self.color_combobox)


        self.layout.addLayout(self.top_layout)

        self.bottom_layout = QGridLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.ring_label = QLabel(self.groupbox)
        self.ring_label.setObjectName(u"ring_label")
        self.ring_label.setFont(font2)
        self.ring_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.ring_label, 3, 2, 1, 1)

        self.point_value_label = QLabel(self.groupbox)
        self.point_value_label.setObjectName(u"point_value_label")
        self.point_value_label.setFont(font2)
        self.point_value_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.point_value_label, 1, 3, 1, 1)

        self.roi_spinbox = QDoubleSpinBox(self.groupbox)
        self.roi_spinbox.setObjectName(u"roi_spinbox")
        self.roi_spinbox.setFont(font2)
        self.roi_spinbox.setAlignment(Qt.AlignCenter)
        self.roi_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.roi_spinbox.setKeyboardTracking(False)
        self.roi_spinbox.setMinimum(0.020000000000000)
        self.roi_spinbox.setMaximum(10.000000000000000)
        self.roi_spinbox.setSingleStep(0.020000000000000)
        self.roi_spinbox.setValue(0.200000000000000)

        self.bottom_layout.addWidget(self.roi_spinbox, 2, 1, 1, 1)

        self.annulus_label = QLabel(self.groupbox)
        self.annulus_label.setObjectName(u"annulus_label")
        self.annulus_label.setFont(font2)
        self.annulus_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.annulus_label, 3, 0, 1, 1)

        self.x_spinbox = QDoubleSpinBox(self.groupbox)
        self.x_spinbox.setObjectName(u"x_spinbox")
        self.x_spinbox.setFont(font2)
        self.x_spinbox.setAlignment(Qt.AlignCenter)
        self.x_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.x_spinbox.setKeyboardTracking(False)
        self.x_spinbox.setMinimum(-100.000000000000000)
        self.x_spinbox.setMaximum(100.000000000000000)
        self.x_spinbox.setSingleStep(0.020000000000000)

        self.bottom_layout.addWidget(self.x_spinbox, 0, 1, 1, 1)

        self.width_spinbox = QDoubleSpinBox(self.groupbox)
        self.width_spinbox.setObjectName(u"width_spinbox")
        self.width_spinbox.setFont(font2)
        self.width_spinbox.setAlignment(Qt.AlignCenter)
        self.width_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.width_spinbox.setKeyboardTracking(False)
        self.width_spinbox.setMinimum(0.010000000000000)
        self.width_spinbox.setMaximum(10.000000000000000)
        self.width_spinbox.setSingleStep(0.010000000000000)
        self.width_spinbox.setValue(0.100000000000000)

        self.bottom_layout.addWidget(self.width_spinbox, 3, 1, 1, 1)

        self.distance_label = QLabel(self.groupbox)
        self.distance_label.setObjectName(u"distance_label")
        self.distance_label.setFont(font2)
        self.distance_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.distance_label, 0, 2, 1, 1)

        self.y_label = QLabel(self.groupbox)
        self.y_label.setObjectName(u"y_label")
        self.y_label.setFont(font2)
        self.y_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.y_label, 1, 0, 1, 1)

        self.roi_label = QLabel(self.groupbox)
        self.roi_label.setObjectName(u"roi_label")
        self.roi_label.setFont(font2)
        self.roi_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.roi_label, 2, 0, 1, 1)

        self.total_area_label = QLabel(self.groupbox)
        self.total_area_label.setObjectName(u"total_area_label")
        self.total_area_label.setFont(font2)
        self.total_area_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.total_area_label, 0, 4, 1, 1)

        self.area_label = QLabel(self.groupbox)
        self.area_label.setObjectName(u"area_label")
        self.area_label.setFont(font2)
        self.area_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.area_label, 2, 2, 1, 1)

        self.y_spinbox = QDoubleSpinBox(self.groupbox)
        self.y_spinbox.setObjectName(u"y_spinbox")
        self.y_spinbox.setFont(font2)
        self.y_spinbox.setAlignment(Qt.AlignCenter)
        self.y_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.y_spinbox.setKeyboardTracking(False)
        self.y_spinbox.setMinimum(-100.000000000000000)
        self.y_spinbox.setMaximum(100.000000000000000)
        self.y_spinbox.setSingleStep(0.020000000000000)

        self.bottom_layout.addWidget(self.y_spinbox, 1, 1, 1, 1)

        self.x_label = QLabel(self.groupbox)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setFont(font2)
        self.x_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.x_label, 0, 0, 1, 1)

        self.area_value_label = QLabel(self.groupbox)
        self.area_value_label.setObjectName(u"area_value_label")
        self.area_value_label.setFont(font2)
        self.area_value_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.area_value_label, 2, 3, 1, 1)

        self.ann_area_label = QLabel(self.groupbox)
        self.ann_area_label.setObjectName(u"ann_area_label")
        self.ann_area_label.setFont(font2)
        self.ann_area_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.ann_area_label, 3, 4, 1, 1)

        self.point_label = QLabel(self.groupbox)
        self.point_label.setObjectName(u"point_label")
        self.point_label.setFont(font2)
        self.point_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.point_label, 1, 2, 1, 1)

        self.distance_value_label = QLabel(self.groupbox)
        self.distance_value_label.setObjectName(u"distance_value_label")
        self.distance_value_label.setFont(font2)
        self.distance_value_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.distance_value_label, 0, 3, 1, 1)

        self.roi_area_label = QLabel(self.groupbox)
        self.roi_area_label.setObjectName(u"roi_area_label")
        self.roi_area_label.setFont(font2)
        self.roi_area_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.roi_area_label, 2, 4, 1, 1)

        self.ring_value_label = QLabel(self.groupbox)
        self.ring_value_label.setObjectName(u"ring_value_label")
        self.ring_value_label.setFont(font2)
        self.ring_value_label.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.ring_value_label, 3, 3, 1, 1)

        self.total_area_value = QLabel(self.groupbox)
        self.total_area_value.setObjectName(u"total_area_value")
        self.total_area_value.setFont(font2)
        self.total_area_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.total_area_value, 0, 5, 1, 1)

        self.ann_area_value = QLabel(self.groupbox)
        self.ann_area_value.setObjectName(u"ann_area_value")
        self.ann_area_value.setFont(font2)
        self.ann_area_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.ann_area_value, 3, 5, 1, 1)

        self.roi_area_value = QLabel(self.groupbox)
        self.roi_area_value.setObjectName(u"roi_area_value")
        self.roi_area_value.setFont(font2)
        self.roi_area_value.setAlignment(Qt.AlignCenter)

        self.bottom_layout.addWidget(self.roi_area_value, 2, 5, 1, 1)


        self.layout.addLayout(self.bottom_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(crosshairannulus)

        QMetaObject.connectSlotsByName(crosshairannulus)
    # setupUi

    def retranslateUi(self, crosshairannulus):
        crosshairannulus.setWindowTitle(QCoreApplication.translate("crosshairannulus", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("crosshairannulus", u"Crosshair", None))
        self.enable_label.setText(QCoreApplication.translate("crosshairannulus", u"Enable:", None))
        self.enable_crosshair_checkbox.setText(QCoreApplication.translate("crosshairannulus", u"Crosshair", None))
        self.enable_roi_checkbox.setText(QCoreApplication.translate("crosshairannulus", u"ROI", None))
        self.enable_annulus_checkbox.setText(QCoreApplication.translate("crosshairannulus", u"Annulus", None))
        self.color_label.setText(QCoreApplication.translate("crosshairannulus", u"Color:", None))
        self.color_combobox.setItemText(0, QCoreApplication.translate("crosshairannulus", u"black", None))
        self.color_combobox.setItemText(1, QCoreApplication.translate("crosshairannulus", u"white", None))
        self.color_combobox.setItemText(2, QCoreApplication.translate("crosshairannulus", u"red", None))
        self.color_combobox.setItemText(3, QCoreApplication.translate("crosshairannulus", u"blue", None))
        self.color_combobox.setItemText(4, QCoreApplication.translate("crosshairannulus", u"green", None))
        self.color_combobox.setItemText(5, QCoreApplication.translate("crosshairannulus", u"cyan", None))
        self.color_combobox.setItemText(6, QCoreApplication.translate("crosshairannulus", u"magenta", None))
        self.color_combobox.setItemText(7, QCoreApplication.translate("crosshairannulus", u"yellow", None))

#if QT_CONFIG(tooltip)
        self.ring_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"<html><head/><body><p>Intensity inside the annulus.</p><p>Depending on the your settings (general settings -&gt; crosshair -&gt; normalized_intensity) the integral of the intensity over the given area is either divided by the area (normalized) or not.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ring_label.setText(QCoreApplication.translate("crosshairannulus", u"Int. (Ann.)", None))
        self.point_value_label.setText("")
        self.annulus_label.setText(QCoreApplication.translate("crosshairannulus", u"Width", None))
#if QT_CONFIG(tooltip)
        self.distance_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"Distance of the crosshair from the origin.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.distance_label.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.distance_label.setText(QCoreApplication.translate("crosshairannulus", u"<html><head/><body><p>k<span style=\"vertical-align:sub;\">||</span></p></body></html>", None))
        self.y_label.setText(QCoreApplication.translate("crosshairannulus", u"y-Pos.", None))
        self.roi_label.setText(QCoreApplication.translate("crosshairannulus", u"Radius", None))
#if QT_CONFIG(tooltip)
        self.total_area_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"Total area (only non-NaN).", None))
#endif // QT_CONFIG(tooltip)
        self.total_area_label.setText(QCoreApplication.translate("crosshairannulus", u"Area (Total)", None))
#if QT_CONFIG(tooltip)
        self.area_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"<html><head/><body><p>Intensity inside the region of interest (ROI).</p><p>Depending on the your settings (general settings -&gt; crosshair -&gt; normalized_intensity) the integral of the intensity over the given area is either divided by the area (normalized) or not.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.area_label.setText(QCoreApplication.translate("crosshairannulus", u"Int. (ROI)", None))
        self.x_label.setText(QCoreApplication.translate("crosshairannulus", u"x-Pos.", None))
        self.area_value_label.setText("")
#if QT_CONFIG(tooltip)
        self.ann_area_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"<html><head/><body><p>(Non-NaN) area inside the annulus.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ann_area_label.setText(QCoreApplication.translate("crosshairannulus", u"Area (Ann.)", None))
#if QT_CONFIG(tooltip)
        self.point_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"Intensity at the crosshair.", None))
#endif // QT_CONFIG(tooltip)
        self.point_label.setText(QCoreApplication.translate("crosshairannulus", u"Int. (Point)", None))
        self.distance_value_label.setText("")
#if QT_CONFIG(tooltip)
        self.roi_area_label.setToolTip(QCoreApplication.translate("crosshairannulus", u"<html><head/><body><p>(Non-NaN) area inside the region of interest (ROI).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.roi_area_label.setText(QCoreApplication.translate("crosshairannulus", u"Area (ROI)", None))
        self.ring_value_label.setText("")
        self.total_area_value.setText("")
        self.ann_area_value.setText("")
        self.roi_area_value.setText("")
    # retranslateUi

