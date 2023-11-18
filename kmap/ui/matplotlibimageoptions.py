# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'matplotlibimageoptions.ui'
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
    QDoubleSpinBox, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QWidget)

class Ui_options(object):
    def setupUi(self, options):
        if not options.objectName():
            options.setObjectName(u"options")
        options.setWindowModality(Qt.WindowModal)
        options.resize(333, 381)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(options.sizePolicy().hasHeightForWidth())
        options.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(options)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.title_line_edit = QLineEdit(options)
        self.title_line_edit.setObjectName(u"title_line_edit")

        self.gridLayout_2.addWidget(self.title_line_edit, 1, 2, 1, 1)

        self.fit_button = QPushButton(options)
        self.fit_button.setObjectName(u"fit_button")

        self.gridLayout_2.addWidget(self.fit_button, 0, 2, 1, 1)

        self.x_max_spinbox = QDoubleSpinBox(options)
        self.x_max_spinbox.setObjectName(u"x_max_spinbox")
        self.x_max_spinbox.setAlignment(Qt.AlignCenter)
        self.x_max_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.x_max_spinbox.setKeyboardTracking(False)
        self.x_max_spinbox.setMinimum(-1.000000000000000)
        self.x_max_spinbox.setMaximum(1000.000000000000000)
        self.x_max_spinbox.setSingleStep(0.100000000000000)
        self.x_max_spinbox.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.x_max_spinbox, 4, 2, 1, 1)

        self.ticks_spinbox = QSpinBox(options)
        self.ticks_spinbox.setObjectName(u"ticks_spinbox")
        self.ticks_spinbox.setAlignment(Qt.AlignCenter)
        self.ticks_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.ticks_spinbox.setKeyboardTracking(False)
        self.ticks_spinbox.setValue(0)

        self.gridLayout_2.addWidget(self.ticks_spinbox, 8, 2, 1, 1)

        self.colorbar_checkbox = QCheckBox(options)
        self.colorbar_checkbox.setObjectName(u"colorbar_checkbox")

        self.gridLayout_2.addWidget(self.colorbar_checkbox, 0, 0, 1, 1)

        self.title_label = QLabel(options)
        self.title_label.setObjectName(u"title_label")

        self.gridLayout_2.addWidget(self.title_label, 1, 0, 1, 1)

        self.x_line_edit = QLineEdit(options)
        self.x_line_edit.setObjectName(u"x_line_edit")

        self.gridLayout_2.addWidget(self.x_line_edit, 2, 2, 1, 1)

        self.y_max_spinbox = QDoubleSpinBox(options)
        self.y_max_spinbox.setObjectName(u"y_max_spinbox")
        self.y_max_spinbox.setAlignment(Qt.AlignCenter)
        self.y_max_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.y_max_spinbox.setKeyboardTracking(False)
        self.y_max_spinbox.setMinimum(-1.000000000000000)
        self.y_max_spinbox.setMaximum(1000.000000000000000)
        self.y_max_spinbox.setSingleStep(0.100000000000000)
        self.y_max_spinbox.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.y_max_spinbox, 7, 2, 1, 1)

        self.x_max_label = QLabel(options)
        self.x_max_label.setObjectName(u"x_max_label")

        self.gridLayout_2.addWidget(self.x_max_label, 4, 0, 1, 1)

        self.y_max_label = QLabel(options)
        self.y_max_label.setObjectName(u"y_max_label")

        self.gridLayout_2.addWidget(self.y_max_label, 7, 0, 1, 1)

        self.x_min_label = QLabel(options)
        self.x_min_label.setObjectName(u"x_min_label")

        self.gridLayout_2.addWidget(self.x_min_label, 3, 0, 1, 1)

        self.x_label_label = QLabel(options)
        self.x_label_label.setObjectName(u"x_label_label")

        self.gridLayout_2.addWidget(self.x_label_label, 2, 0, 1, 1)

        self.y_line_edit = QLineEdit(options)
        self.y_line_edit.setObjectName(u"y_line_edit")
        self.y_line_edit.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.y_line_edit, 5, 2, 1, 1)

        self.y_min_spinbox = QDoubleSpinBox(options)
        self.y_min_spinbox.setObjectName(u"y_min_spinbox")
        self.y_min_spinbox.setAlignment(Qt.AlignCenter)
        self.y_min_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.y_min_spinbox.setKeyboardTracking(False)
        self.y_min_spinbox.setMinimum(-1000.000000000000000)
        self.y_min_spinbox.setMaximum(1.000000000000000)
        self.y_min_spinbox.setSingleStep(0.100000000000000)
        self.y_min_spinbox.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.y_min_spinbox, 6, 2, 1, 1)

        self.grid_label = QLabel(options)
        self.grid_label.setObjectName(u"grid_label")

        self.gridLayout_2.addWidget(self.grid_label, 12, 0, 1, 1)

        self.y_label_label = QLabel(options)
        self.y_label_label.setObjectName(u"y_label_label")

        self.gridLayout_2.addWidget(self.y_label_label, 5, 0, 1, 1)

        self.grid_combobox = QComboBox(options)
        self.grid_combobox.addItem("")
        self.grid_combobox.addItem("")
        self.grid_combobox.addItem("")
        self.grid_combobox.setObjectName(u"grid_combobox")
        self.grid_combobox.setMaxVisibleItems(3)
        self.grid_combobox.setMaxCount(3)

        self.gridLayout_2.addWidget(self.grid_combobox, 12, 2, 1, 1)

        self.x_min_spinbox = QDoubleSpinBox(options)
        self.x_min_spinbox.setObjectName(u"x_min_spinbox")
        self.x_min_spinbox.setAlignment(Qt.AlignCenter)
        self.x_min_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.x_min_spinbox.setKeyboardTracking(False)
        self.x_min_spinbox.setMinimum(-1000.000000000000000)
        self.x_min_spinbox.setMaximum(1.000000000000000)
        self.x_min_spinbox.setSingleStep(0.100000000000000)
        self.x_min_spinbox.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.x_min_spinbox, 3, 2, 1, 1)

        self.ticks_label = QLabel(options)
        self.ticks_label.setObjectName(u"ticks_label")

        self.gridLayout_2.addWidget(self.ticks_label, 8, 0, 1, 1)

        self.y_min_label = QLabel(options)
        self.y_min_label.setObjectName(u"y_min_label")

        self.gridLayout_2.addWidget(self.y_min_label, 6, 0, 1, 1)


        self.retranslateUi(options)

        self.grid_combobox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(options)
    # setupUi

    def retranslateUi(self, options):
        options.setWindowTitle(QCoreApplication.translate("options", u"Options", None))
        self.title_line_edit.setPlaceholderText(QCoreApplication.translate("options", u"Enter title here...", None))
        self.fit_button.setText(QCoreApplication.translate("options", u"Fit Axis", None))
        self.colorbar_checkbox.setText(QCoreApplication.translate("options", u"Add Colorbar", None))
        self.title_label.setText(QCoreApplication.translate("options", u"Title", None))
        self.x_line_edit.setPlaceholderText(QCoreApplication.translate("options", u"Enter label here...", None))
        self.x_max_label.setText(QCoreApplication.translate("options", u"x-Axis Max.", None))
        self.y_max_label.setText(QCoreApplication.translate("options", u"y-Axis Max.", None))
        self.x_min_label.setText(QCoreApplication.translate("options", u"x-Axis Min.", None))
        self.x_label_label.setText(QCoreApplication.translate("options", u"x-Axis Label", None))
        self.y_line_edit.setPlaceholderText(QCoreApplication.translate("options", u"Enter label here...", None))
        self.grid_label.setText(QCoreApplication.translate("options", u"Grid Density", None))
        self.y_label_label.setText(QCoreApplication.translate("options", u"y-Axis Label", None))
        self.grid_combobox.setItemText(0, QCoreApplication.translate("options", u"No Grid", None))
        self.grid_combobox.setItemText(1, QCoreApplication.translate("options", u"Major Only", None))
        self.grid_combobox.setItemText(2, QCoreApplication.translate("options", u"Major and Minor", None))

        self.ticks_label.setText(QCoreApplication.translate("options", u"Minor Ticks", None))
        self.y_min_label.setText(QCoreApplication.translate("options", u"y-Axis Min.", None))
    # retranslateUi

