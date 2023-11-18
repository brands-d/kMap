# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profileplottab.ui'
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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from kmap.controller.profileplot import ProfilePlot

class Ui_profileplottab(object):
    def setupUi(self, profileplottab):
        if not profileplottab.objectName():
            profileplottab.setObjectName(u"profileplottab")
        profileplottab.resize(1213, 927)
        self.horizontalLayout = QHBoxLayout(profileplottab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scroll_area = QScrollArea(profileplottab)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setMinimumSize(QSize(300, 0))
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 298, 903))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabs_groupbox = QGroupBox(self.scrollAreaWidgetContents)
        self.tabs_groupbox.setObjectName(u"tabs_groupbox")
        font = QFont()
        font.setBold(True)
        self.tabs_groupbox.setFont(font)
        self.tabs_groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_4 = QVBoxLayout(self.tabs_groupbox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 15, 5, 5)
        self.tab_combobox = QComboBox(self.tabs_groupbox)
        self.tab_combobox.setObjectName(u"tab_combobox")
        font1 = QFont()
        font1.setBold(False)
        self.tab_combobox.setFont(font1)
        self.tab_combobox.setInsertPolicy(QComboBox.InsertAtBottom)

        self.verticalLayout_4.addWidget(self.tab_combobox)

        self.center_checkbox = QCheckBox(self.tabs_groupbox)
        self.center_checkbox.setObjectName(u"center_checkbox")
        self.center_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.center_checkbox)

        self.x_checkbox = QCheckBox(self.tabs_groupbox)
        self.x_checkbox.setObjectName(u"x_checkbox")
        self.x_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.x_checkbox)

        self.y_checkbox = QCheckBox(self.tabs_groupbox)
        self.y_checkbox.setObjectName(u"y_checkbox")
        self.y_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.y_checkbox)

        self.roi_checkbox = QCheckBox(self.tabs_groupbox)
        self.roi_checkbox.setObjectName(u"roi_checkbox")
        self.roi_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.roi_checkbox)

        self.border_checkbox = QCheckBox(self.tabs_groupbox)
        self.border_checkbox.setObjectName(u"border_checkbox")
        self.border_checkbox.setEnabled(True)
        self.border_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.border_checkbox)

        self.annulus_checkbox = QCheckBox(self.tabs_groupbox)
        self.annulus_checkbox.setObjectName(u"annulus_checkbox")
        self.annulus_checkbox.setFont(font1)

        self.verticalLayout_4.addWidget(self.annulus_checkbox)


        self.verticalLayout.addWidget(self.tabs_groupbox)

        self.options_groupbox = QGroupBox(self.scrollAreaWidgetContents)
        self.options_groupbox.setObjectName(u"options_groupbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.options_groupbox.sizePolicy().hasHeightForWidth())
        self.options_groupbox.setSizePolicy(sizePolicy1)
        self.options_groupbox.setFont(font)
        self.options_groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.options_groupbox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 15, 5, 5)
        self.layout = QVBoxLayout()
        self.layout.setObjectName(u"layout")
        self.line_radiobutton = QRadioButton(self.options_groupbox)
        self.line_radiobutton.setObjectName(u"line_radiobutton")
        self.line_radiobutton.setFont(font1)
        self.line_radiobutton.setChecked(True)

        self.layout.addWidget(self.line_radiobutton)

        self.circle_radiobutton = QRadioButton(self.options_groupbox)
        self.circle_radiobutton.setObjectName(u"circle_radiobutton")
        self.circle_radiobutton.setFont(font1)

        self.layout.addWidget(self.circle_radiobutton)

        self.slice_radiobutton = QRadioButton(self.options_groupbox)
        self.slice_radiobutton.setObjectName(u"slice_radiobutton")
        self.slice_radiobutton.setFont(font1)

        self.layout.addWidget(self.slice_radiobutton)

        self.normalize_checkbox = QCheckBox(self.options_groupbox)
        self.normalize_checkbox.setObjectName(u"normalize_checkbox")
        self.normalize_checkbox.setFont(font1)
        self.normalize_checkbox.setChecked(True)

        self.layout.addWidget(self.normalize_checkbox)

        self.layout_2 = QGridLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.phi_sample_label = QLabel(self.options_groupbox)
        self.phi_sample_label.setObjectName(u"phi_sample_label")
        self.phi_sample_label.setFont(font1)

        self.layout_2.addWidget(self.phi_sample_label, 0, 0, 1, 1)

        self.phi_sample_spinbox = QSpinBox(self.options_groupbox)
        self.phi_sample_spinbox.setObjectName(u"phi_sample_spinbox")
        self.phi_sample_spinbox.setFont(font1)
        self.phi_sample_spinbox.setAlignment(Qt.AlignCenter)
        self.phi_sample_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.phi_sample_spinbox.setKeyboardTracking(False)
        self.phi_sample_spinbox.setMinimum(1)
        self.phi_sample_spinbox.setMaximum(1440)
        self.phi_sample_spinbox.setSingleStep(10)
        self.phi_sample_spinbox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.phi_sample_spinbox.setValue(720)

        self.layout_2.addWidget(self.phi_sample_spinbox, 0, 1, 1, 1)

        self.line_sample_spinbox = QSpinBox(self.options_groupbox)
        self.line_sample_spinbox.setObjectName(u"line_sample_spinbox")
        self.line_sample_spinbox.setFont(font1)
        self.line_sample_spinbox.setAlignment(Qt.AlignCenter)
        self.line_sample_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.line_sample_spinbox.setKeyboardTracking(False)
        self.line_sample_spinbox.setMinimum(1)
        self.line_sample_spinbox.setMaximum(1000)
        self.line_sample_spinbox.setSingleStep(10)
        self.line_sample_spinbox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.line_sample_spinbox.setValue(500)

        self.layout_2.addWidget(self.line_sample_spinbox, 1, 1, 1, 1)

        self.line_sample_label = QLabel(self.options_groupbox)
        self.line_sample_label.setObjectName(u"line_sample_label")
        self.line_sample_label.setFont(font1)

        self.layout_2.addWidget(self.line_sample_label, 1, 0, 1, 1)


        self.layout.addLayout(self.layout_2)


        self.verticalLayout_2.addLayout(self.layout)

        self.refresh_button = QPushButton(self.options_groupbox)
        self.refresh_button.setObjectName(u"refresh_button")
        self.refresh_button.setFont(font1)

        self.verticalLayout_2.addWidget(self.refresh_button)


        self.verticalLayout.addWidget(self.options_groupbox)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacer)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scroll_area)

        self.plot_item = ProfilePlot(profileplottab)
        self.plot_item.setObjectName(u"plot_item")

        self.horizontalLayout.addWidget(self.plot_item)


        self.retranslateUi(profileplottab)

        QMetaObject.connectSlotsByName(profileplottab)
    # setupUi

    def retranslateUi(self, profileplottab):
        profileplottab.setWindowTitle(QCoreApplication.translate("profileplottab", u"Form", None))
        self.tabs_groupbox.setTitle(QCoreApplication.translate("profileplottab", u"Tabs", None))
        self.center_checkbox.setText(QCoreApplication.translate("profileplottab", u"Center Point", None))
        self.x_checkbox.setText(QCoreApplication.translate("profileplottab", u"Vertical Line", None))
        self.y_checkbox.setText(QCoreApplication.translate("profileplottab", u"Horizontal Line", None))
        self.roi_checkbox.setText(QCoreApplication.translate("profileplottab", u"ROI", None))
        self.border_checkbox.setText(QCoreApplication.translate("profileplottab", u"ROI Border", None))
        self.annulus_checkbox.setText(QCoreApplication.translate("profileplottab", u"Annulus", None))
        self.options_groupbox.setTitle(QCoreApplication.translate("profileplottab", u"Options", None))
        self.line_radiobutton.setText(QCoreApplication.translate("profileplottab", u"Line Like Plot", None))
        self.circle_radiobutton.setText(QCoreApplication.translate("profileplottab", u"Circle Like Plot", None))
        self.slice_radiobutton.setText(QCoreApplication.translate("profileplottab", u"Slice Like Plot", None))
        self.normalize_checkbox.setText(QCoreApplication.translate("profileplottab", u"Normalized", None))
        self.phi_sample_label.setText(QCoreApplication.translate("profileplottab", u"Phi Sample Points:", None))
        self.line_sample_label.setText(QCoreApplication.translate("profileplottab", u"Line Sample Points:", None))
        self.refresh_button.setText(QCoreApplication.translate("profileplottab", u"Refresh Plot", None))
    # retranslateUi

