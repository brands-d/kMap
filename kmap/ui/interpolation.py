# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interpolation.ui'
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
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_interpolation(object):
    def setupUi(self, interpolation):
        if not interpolation.objectName():
            interpolation.setObjectName(u"interpolation")
        interpolation.resize(686, 446)
        self.horizontalLayout = QHBoxLayout(interpolation)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupbox = QGroupBox(interpolation)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.groupbox)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 15, 5, 0)
        self.layout_5 = QVBoxLayout()
        self.layout_5.setObjectName(u"layout_5")
        self.layout_6 = QHBoxLayout()
        self.layout_6.setObjectName(u"layout_6")
        self.interpolation_checkbox = QCheckBox(self.groupbox)
        self.interpolation_checkbox.setObjectName(u"interpolation_checkbox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolation_checkbox.sizePolicy().hasHeightForWidth())
        self.interpolation_checkbox.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(False)
        self.interpolation_checkbox.setFont(font1)

        self.layout_6.addWidget(self.interpolation_checkbox)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_6.addItem(self.spacer)

        self.order_label = QLabel(self.groupbox)
        self.order_label.setObjectName(u"order_label")
        self.order_label.setEnabled(False)
        self.order_label.setFont(font1)
        self.order_label.setAlignment(Qt.AlignCenter)

        self.layout_6.addWidget(self.order_label)

        self.order_spinbox = QSpinBox(self.groupbox)
        self.order_spinbox.setObjectName(u"order_spinbox")
        self.order_spinbox.setEnabled(False)
        self.order_spinbox.setFont(font1)
        self.order_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.order_spinbox.setKeyboardTracking(False)
        self.order_spinbox.setMinimum(1)
        self.order_spinbox.setMaximum(5)
        self.order_spinbox.setValue(1)

        self.layout_6.addWidget(self.order_spinbox)


        self.layout_5.addLayout(self.layout_6)

        self.layout_2 = QHBoxLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.smoothing_checkbox = QCheckBox(self.groupbox)
        self.smoothing_checkbox.setObjectName(u"smoothing_checkbox")
        self.smoothing_checkbox.setFont(font1)

        self.layout_2.addWidget(self.smoothing_checkbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_2.addItem(self.horizontalSpacer)

        self.fill_label = QLabel(self.groupbox)
        self.fill_label.setObjectName(u"fill_label")
        self.fill_label.setFont(font1)

        self.layout_2.addWidget(self.fill_label)

        self.fill_combobox = QComboBox(self.groupbox)
        self.fill_combobox.addItem("")
        self.fill_combobox.addItem("")
        self.fill_combobox.addItem("")
        self.fill_combobox.setObjectName(u"fill_combobox")
        self.fill_combobox.setFont(font1)
        self.fill_combobox.setMaxVisibleItems(3)
        self.fill_combobox.setMaxCount(3)

        self.layout_2.addWidget(self.fill_combobox)


        self.layout_5.addLayout(self.layout_2)


        self.verticalLayout.addLayout(self.layout_5)

        self.layout_3 = QGridLayout()
        self.layout_3.setObjectName(u"layout_3")
        self.y_resolution_spinbox = QDoubleSpinBox(self.groupbox)
        self.y_resolution_spinbox.setObjectName(u"y_resolution_spinbox")
        self.y_resolution_spinbox.setFont(font1)
        self.y_resolution_spinbox.setAlignment(Qt.AlignCenter)
        self.y_resolution_spinbox.setMinimum(0.010000000000000)
        self.y_resolution_spinbox.setMaximum(0.100000000000000)
        self.y_resolution_spinbox.setSingleStep(0.010000000000000)
        self.y_resolution_spinbox.setValue(0.030000000000000)

        self.layout_3.addWidget(self.y_resolution_spinbox, 2, 1, 1, 1)

        self.y_label = QLabel(self.groupbox)
        self.y_label.setObjectName(u"y_label")
        self.y_label.setFont(font1)
        self.y_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.y_label, 2, 0, 1, 1)

        self.x_resolution_spinbox = QDoubleSpinBox(self.groupbox)
        self.x_resolution_spinbox.setObjectName(u"x_resolution_spinbox")
        sizePolicy.setHeightForWidth(self.x_resolution_spinbox.sizePolicy().hasHeightForWidth())
        self.x_resolution_spinbox.setSizePolicy(sizePolicy)
        self.x_resolution_spinbox.setFont(font1)
        self.x_resolution_spinbox.setAlignment(Qt.AlignCenter)
        self.x_resolution_spinbox.setMinimum(0.010000000000000)
        self.x_resolution_spinbox.setMaximum(0.100000000000000)
        self.x_resolution_spinbox.setSingleStep(0.010000000000000)
        self.x_resolution_spinbox.setValue(0.030000000000000)

        self.layout_3.addWidget(self.x_resolution_spinbox, 1, 1, 1, 1)

        self.resolution_label = QLabel(self.groupbox)
        self.resolution_label.setObjectName(u"resolution_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resolution_label.sizePolicy().hasHeightForWidth())
        self.resolution_label.setSizePolicy(sizePolicy1)
        self.resolution_label.setFont(font1)
        self.resolution_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.resolution_label, 0, 1, 1, 1)

        self.x_label = QLabel(self.groupbox)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setFont(font1)
        self.x_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.x_label, 1, 0, 1, 1)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.x_min_spinbox = QDoubleSpinBox(self.groupbox)
        self.x_min_spinbox.setObjectName(u"x_min_spinbox")
        self.x_min_spinbox.setFont(font1)
        self.x_min_spinbox.setAlignment(Qt.AlignCenter)
        self.x_min_spinbox.setDecimals(1)
        self.x_min_spinbox.setMinimum(-50.000000000000000)
        self.x_min_spinbox.setMaximum(50.000000000000000)
        self.x_min_spinbox.setSingleStep(0.100000000000000)
        self.x_min_spinbox.setValue(-3.000000000000000)

        self.layout.addWidget(self.x_min_spinbox)

        self.x_max_spinbox = QDoubleSpinBox(self.groupbox)
        self.x_max_spinbox.setObjectName(u"x_max_spinbox")
        self.x_max_spinbox.setFont(font1)
        self.x_max_spinbox.setAlignment(Qt.AlignCenter)
        self.x_max_spinbox.setDecimals(1)
        self.x_max_spinbox.setMinimum(-50.000000000000000)
        self.x_max_spinbox.setMaximum(50.000000000000000)
        self.x_max_spinbox.setSingleStep(0.100000000000000)
        self.x_max_spinbox.setValue(3.000000000000000)

        self.layout.addWidget(self.x_max_spinbox)


        self.layout_3.addLayout(self.layout, 1, 2, 1, 1)

        self.layout_4 = QHBoxLayout()
        self.layout_4.setObjectName(u"layout_4")
        self.y_min_spinbox = QDoubleSpinBox(self.groupbox)
        self.y_min_spinbox.setObjectName(u"y_min_spinbox")
        self.y_min_spinbox.setFont(font1)
        self.y_min_spinbox.setAlignment(Qt.AlignCenter)
        self.y_min_spinbox.setDecimals(1)
        self.y_min_spinbox.setMinimum(-50.000000000000000)
        self.y_min_spinbox.setMaximum(50.000000000000000)
        self.y_min_spinbox.setSingleStep(0.100000000000000)
        self.y_min_spinbox.setValue(-3.000000000000000)

        self.layout_4.addWidget(self.y_min_spinbox)

        self.y_max_spinbox = QDoubleSpinBox(self.groupbox)
        self.y_max_spinbox.setObjectName(u"y_max_spinbox")
        self.y_max_spinbox.setFont(font1)
        self.y_max_spinbox.setAlignment(Qt.AlignCenter)
        self.y_max_spinbox.setDecimals(1)
        self.y_max_spinbox.setMinimum(-50.000000000000000)
        self.y_max_spinbox.setMaximum(50.000000000000000)
        self.y_max_spinbox.setSingleStep(0.100000000000000)
        self.y_max_spinbox.setValue(3.000000000000000)

        self.layout_4.addWidget(self.y_max_spinbox)


        self.layout_3.addLayout(self.layout_4, 2, 2, 1, 1)

        self.range_label = QLabel(self.groupbox)
        self.range_label.setObjectName(u"range_label")
        sizePolicy1.setHeightForWidth(self.range_label.sizePolicy().hasHeightForWidth())
        self.range_label.setSizePolicy(sizePolicy1)
        self.range_label.setFont(font1)
        self.range_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.range_label, 0, 2, 1, 1)

        self.sigma_label = QLabel(self.groupbox)
        self.sigma_label.setObjectName(u"sigma_label")
        sizePolicy1.setHeightForWidth(self.sigma_label.sizePolicy().hasHeightForWidth())
        self.sigma_label.setSizePolicy(sizePolicy1)
        self.sigma_label.setFont(font1)
        self.sigma_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.sigma_label, 0, 3, 1, 1)

        self.sigma_x_spinbox = QDoubleSpinBox(self.groupbox)
        self.sigma_x_spinbox.setObjectName(u"sigma_x_spinbox")
        self.sigma_x_spinbox.setFont(font1)
        self.sigma_x_spinbox.setAlignment(Qt.AlignCenter)
        self.sigma_x_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.sigma_x_spinbox.setKeyboardTracking(False)
        self.sigma_x_spinbox.setDecimals(2)
        self.sigma_x_spinbox.setMaximum(100.000000000000000)
        self.sigma_x_spinbox.setSingleStep(0.010000000000000)
        self.sigma_x_spinbox.setValue(0.000000000000000)

        self.layout_3.addWidget(self.sigma_x_spinbox, 1, 3, 1, 1)

        self.sigma_y_spinbox = QDoubleSpinBox(self.groupbox)
        self.sigma_y_spinbox.setObjectName(u"sigma_y_spinbox")
        self.sigma_y_spinbox.setFont(font1)
        self.sigma_y_spinbox.setAlignment(Qt.AlignCenter)
        self.sigma_y_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.sigma_y_spinbox.setKeyboardTracking(False)
        self.sigma_y_spinbox.setDecimals(2)
        self.sigma_y_spinbox.setMaximum(100.000000000000000)
        self.sigma_y_spinbox.setSingleStep(0.010000000000000)
        self.sigma_y_spinbox.setValue(0.000000000000000)

        self.layout_3.addWidget(self.sigma_y_spinbox, 2, 3, 1, 1)

        self.layout_3.setColumnStretch(0, 1)
        self.layout_3.setColumnStretch(1, 1)
        self.layout_3.setColumnStretch(2, 2)
        self.layout_3.setColumnStretch(3, 1)

        self.verticalLayout.addLayout(self.layout_3)

        self.spacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacer_2)

        self.verticalLayout.setStretch(2, 1)

        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(interpolation)

        QMetaObject.connectSlotsByName(interpolation)
    # setupUi

    def retranslateUi(self, interpolation):
        interpolation.setWindowTitle(QCoreApplication.translate("interpolation", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("interpolation", u"Interpolation", None))
        self.interpolation_checkbox.setText(QCoreApplication.translate("interpolation", u"Interpolation", None))
#if QT_CONFIG(tooltip)
        self.order_label.setToolTip(QCoreApplication.translate("interpolation", u"NOT IMPLEMENTED", None))
#endif // QT_CONFIG(tooltip)
        self.order_label.setText(QCoreApplication.translate("interpolation", u"Order:", None))
#if QT_CONFIG(tooltip)
        self.order_spinbox.setToolTip(QCoreApplication.translate("interpolation", u"NOT IMPLEMENTED", None))
#endif // QT_CONFIG(tooltip)
        self.smoothing_checkbox.setText(QCoreApplication.translate("interpolation", u"Gaussian Filter", None))
        self.fill_label.setText(QCoreApplication.translate("interpolation", u"Fill Value:", None))
        self.fill_combobox.setItemText(0, QCoreApplication.translate("interpolation", u"Mean", None))
        self.fill_combobox.setItemText(1, QCoreApplication.translate("interpolation", u"Zero", None))
        self.fill_combobox.setItemText(2, QCoreApplication.translate("interpolation", u"NaN", None))

        self.y_label.setText(QCoreApplication.translate("interpolation", u"y-Axis:", None))
        self.resolution_label.setText(QCoreApplication.translate("interpolation", u"Resolution:", None))
        self.x_label.setText(QCoreApplication.translate("interpolation", u"x-Axis:", None))
        self.range_label.setText(QCoreApplication.translate("interpolation", u"Range (min/max):", None))
        self.sigma_label.setText(QCoreApplication.translate("interpolation", u"Sigma:", None))
    # retranslateUi

