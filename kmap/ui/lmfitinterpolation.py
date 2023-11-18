# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitinterpolation.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_lmfitinterpolation(object):
    def setupUi(self, lmfitinterpolation):
        if not lmfitinterpolation.objectName():
            lmfitinterpolation.setObjectName(u"lmfitinterpolation")
        lmfitinterpolation.resize(609, 101)
        self.horizontalLayout = QHBoxLayout(lmfitinterpolation)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupbox = QGroupBox(lmfitinterpolation)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.groupbox)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.layout_3 = QGridLayout()
        self.layout_3.setObjectName(u"layout_3")
        self.resolution_label = QLabel(self.groupbox)
        self.resolution_label.setObjectName(u"resolution_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resolution_label.sizePolicy().hasHeightForWidth())
        self.resolution_label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(False)
        self.resolution_label.setFont(font1)
        self.resolution_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.resolution_label, 0, 1, 1, 1)

        self.resolution_spinbox = QDoubleSpinBox(self.groupbox)
        self.resolution_spinbox.setObjectName(u"resolution_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resolution_spinbox.sizePolicy().hasHeightForWidth())
        self.resolution_spinbox.setSizePolicy(sizePolicy1)
        self.resolution_spinbox.setFont(font1)
        self.resolution_spinbox.setAlignment(Qt.AlignCenter)
        self.resolution_spinbox.setKeyboardTracking(False)
        self.resolution_spinbox.setMinimum(0.010000000000000)
        self.resolution_spinbox.setMaximum(0.100000000000000)
        self.resolution_spinbox.setSingleStep(0.010000000000000)
        self.resolution_spinbox.setValue(0.030000000000000)

        self.layout_3.addWidget(self.resolution_spinbox, 1, 1, 1, 1)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.min_spinbox = QDoubleSpinBox(self.groupbox)
        self.min_spinbox.setObjectName(u"min_spinbox")
        self.min_spinbox.setFont(font1)
        self.min_spinbox.setAlignment(Qt.AlignCenter)
        self.min_spinbox.setKeyboardTracking(False)
        self.min_spinbox.setDecimals(1)
        self.min_spinbox.setMinimum(-50.000000000000000)
        self.min_spinbox.setMaximum(50.000000000000000)
        self.min_spinbox.setSingleStep(0.100000000000000)
        self.min_spinbox.setValue(-3.000000000000000)

        self.layout.addWidget(self.min_spinbox)

        self.max_spinbox = QDoubleSpinBox(self.groupbox)
        self.max_spinbox.setObjectName(u"max_spinbox")
        self.max_spinbox.setFont(font1)
        self.max_spinbox.setAlignment(Qt.AlignCenter)
        self.max_spinbox.setKeyboardTracking(False)
        self.max_spinbox.setDecimals(1)
        self.max_spinbox.setMinimum(-50.000000000000000)
        self.max_spinbox.setMaximum(50.000000000000000)
        self.max_spinbox.setSingleStep(0.100000000000000)
        self.max_spinbox.setValue(3.000000000000000)

        self.layout.addWidget(self.max_spinbox)


        self.layout_3.addLayout(self.layout, 1, 2, 1, 1)

        self.range_label = QLabel(self.groupbox)
        self.range_label.setObjectName(u"range_label")
        sizePolicy.setHeightForWidth(self.range_label.sizePolicy().hasHeightForWidth())
        self.range_label.setSizePolicy(sizePolicy)
        self.range_label.setFont(font1)
        self.range_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.range_label, 0, 2, 1, 1)

        self.label = QLabel(self.groupbox)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.label, 1, 0, 1, 1)

        self.interpolation_checkbox = QCheckBox(self.groupbox)
        self.interpolation_checkbox.setObjectName(u"interpolation_checkbox")
        self.interpolation_checkbox.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.interpolation_checkbox.sizePolicy().hasHeightForWidth())
        self.interpolation_checkbox.setSizePolicy(sizePolicy1)
        self.interpolation_checkbox.setFont(font1)
        self.interpolation_checkbox.setChecked(True)

        self.layout_3.addWidget(self.interpolation_checkbox, 0, 0, 1, 1)

        self.layout_3.setColumnStretch(0, 1)
        self.layout_3.setColumnStretch(1, 1)
        self.layout_3.setColumnStretch(2, 2)

        self.verticalLayout.addLayout(self.layout_3)

        self.spacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacer_2)

        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(lmfitinterpolation)

        QMetaObject.connectSlotsByName(lmfitinterpolation)
    # setupUi

    def retranslateUi(self, lmfitinterpolation):
        lmfitinterpolation.setWindowTitle(QCoreApplication.translate("lmfitinterpolation", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("lmfitinterpolation", u"Interpolation", None))
        self.resolution_label.setText(QCoreApplication.translate("lmfitinterpolation", u"Resolution:", None))
        self.range_label.setText(QCoreApplication.translate("lmfitinterpolation", u"Range (min/max):", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("lmfitinterpolation", u"LMFit only supports square kmaps. This setting\n"
"applies for both axes.", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("lmfitinterpolation", u"Axes:", None))
#if QT_CONFIG(tooltip)
        self.interpolation_checkbox.setToolTip(QCoreApplication.translate("lmfitinterpolation", u"Interpolation can not be disabled for LMFit as it provides the common grid for the SlicedData and\n"
"the OrbitalData.", None))
#endif // QT_CONFIG(tooltip)
        self.interpolation_checkbox.setText(QCoreApplication.translate("lmfitinterpolation", u"Interpolation", None))
    # retranslateUi

