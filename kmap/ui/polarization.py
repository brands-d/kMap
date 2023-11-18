# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'polarization.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_polarization(object):
    def setupUi(self, polarization):
        if not polarization.objectName():
            polarization.setObjectName(u"polarization")
        polarization.resize(349, 194)
        self.verticalLayout = QVBoxLayout(polarization)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.groupbox = QGroupBox(polarization)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.groupbox)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 15, 5, 0)
        self.polarization_combobox = QComboBox(self.groupbox)
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.setObjectName(u"polarization_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarization_combobox.sizePolicy().hasHeightForWidth())
        self.polarization_combobox.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(False)
        self.polarization_combobox.setFont(font1)

        self.gridLayout.addWidget(self.polarization_combobox, 1, 1, 1, 1)

        self.polarization_label = QLabel(self.groupbox)
        self.polarization_label.setObjectName(u"polarization_label")
        self.polarization_label.setFont(font1)

        self.gridLayout.addWidget(self.polarization_label, 1, 0, 1, 1)

        self.angle_spinbox = QDoubleSpinBox(self.groupbox)
        self.angle_spinbox.setObjectName(u"angle_spinbox")
        sizePolicy.setHeightForWidth(self.angle_spinbox.sizePolicy().hasHeightForWidth())
        self.angle_spinbox.setSizePolicy(sizePolicy)
        self.angle_spinbox.setFont(font1)
        self.angle_spinbox.setAlignment(Qt.AlignCenter)
        self.angle_spinbox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.angle_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.angle_spinbox.setKeyboardTracking(False)
        self.angle_spinbox.setDecimals(1)
        self.angle_spinbox.setMaximum(90.000000000000000)
        self.angle_spinbox.setSingleStep(1.000000000000000)
        self.angle_spinbox.setValue(45.000000000000000)

        self.gridLayout.addWidget(self.angle_spinbox, 3, 1, 1, 1)

        self.azimuth_spinbox = QDoubleSpinBox(self.groupbox)
        self.azimuth_spinbox.setObjectName(u"azimuth_spinbox")
        sizePolicy.setHeightForWidth(self.azimuth_spinbox.sizePolicy().hasHeightForWidth())
        self.azimuth_spinbox.setSizePolicy(sizePolicy)
        self.azimuth_spinbox.setFont(font1)
        self.azimuth_spinbox.setAlignment(Qt.AlignCenter)
        self.azimuth_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.azimuth_spinbox.setKeyboardTracking(False)
        self.azimuth_spinbox.setDecimals(1)
        self.azimuth_spinbox.setMaximum(360.000000000000000)

        self.gridLayout.addWidget(self.azimuth_spinbox, 5, 1, 1, 1)

        self.ak_label = QLabel(self.groupbox)
        self.ak_label.setObjectName(u"ak_label")
        self.ak_label.setEnabled(True)
        self.ak_label.setFont(font1)

        self.gridLayout.addWidget(self.ak_label, 0, 0, 1, 1)

        self.ak_combobox = QComboBox(self.groupbox)
        self.ak_combobox.addItem("")
        self.ak_combobox.addItem("")
        self.ak_combobox.addItem("")
        self.ak_combobox.setObjectName(u"ak_combobox")
        self.ak_combobox.setEnabled(True)
        sizePolicy.setHeightForWidth(self.ak_combobox.sizePolicy().hasHeightForWidth())
        self.ak_combobox.setSizePolicy(sizePolicy)
        self.ak_combobox.setFont(font1)
        self.ak_combobox.setMaxVisibleItems(3)
        self.ak_combobox.setMaxCount(3)

        self.gridLayout.addWidget(self.ak_combobox, 0, 1, 1, 1)

        self.angle_label = QLabel(self.groupbox)
        self.angle_label.setObjectName(u"angle_label")
        self.angle_label.setFont(font1)

        self.gridLayout.addWidget(self.angle_label, 3, 0, 1, 1)

        self.azimuth_label = QLabel(self.groupbox)
        self.azimuth_label.setObjectName(u"azimuth_label")
        self.azimuth_label.setFont(font1)

        self.gridLayout.addWidget(self.azimuth_label, 5, 0, 1, 1)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.spacer, 6, 0, 1, 1)

        self.s_share_label = QLabel(self.groupbox)
        self.s_share_label.setObjectName(u"s_share_label")
        self.s_share_label.setFont(font1)

        self.gridLayout.addWidget(self.s_share_label, 2, 0, 1, 1)

        self.s_share_spinbox = QDoubleSpinBox(self.groupbox)
        self.s_share_spinbox.setObjectName(u"s_share_spinbox")
        self.s_share_spinbox.setFont(font1)
        self.s_share_spinbox.setAlignment(Qt.AlignCenter)
        self.s_share_spinbox.setKeyboardTracking(False)
        self.s_share_spinbox.setDecimals(3)
        self.s_share_spinbox.setMinimum(0.000000000000000)
        self.s_share_spinbox.setMaximum(1.000000000000000)
        self.s_share_spinbox.setMinimum(0.000000000000000)
        self.s_share_spinbox.setSingleStep(0.010000000000000)
        self.s_share_spinbox.setValue(0.694000000000000)

        self.gridLayout.addWidget(self.s_share_spinbox, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupbox)


        self.retranslateUi(polarization)

        self.polarization_combobox.setCurrentIndex(0)
        self.ak_combobox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(polarization)
    # setupUi

    def retranslateUi(self, polarization):
        polarization.setWindowTitle(QCoreApplication.translate("polarization", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("polarization", u"Polarization", None))
        self.polarization_combobox.setItemText(0, QCoreApplication.translate("polarization", u"Toroid (p-pol)", None))
        self.polarization_combobox.setItemText(1, QCoreApplication.translate("polarization", u"p-polarized", None))
        self.polarization_combobox.setItemText(2, QCoreApplication.translate("polarization", u"s-polarized", None))
        self.polarization_combobox.setItemText(3, QCoreApplication.translate("polarization", u"unpolarized", None))
        self.polarization_combobox.setItemText(4, QCoreApplication.translate("polarization", u"circular+", None))
        self.polarization_combobox.setItemText(5, QCoreApplication.translate("polarization", u"circular-", None))
        self.polarization_combobox.setItemText(6, QCoreApplication.translate("polarization", u"CDAD", None))

#if QT_CONFIG(tooltip)
        self.polarization_combobox.setToolTip(QCoreApplication.translate("polarization", u"Choose one type of polarization.", None))
#endif // QT_CONFIG(tooltip)
        self.polarization_label.setText(QCoreApplication.translate("polarization", u"Polarization:", None))
#if QT_CONFIG(tooltip)
        self.angle_spinbox.setToolTip(QCoreApplication.translate("polarization", u"The angle of incidence.", None))
#endif // QT_CONFIG(tooltip)
        self.angle_spinbox.setSuffix(QCoreApplication.translate("polarization", u"\u00b0", None))
#if QT_CONFIG(tooltip)
        self.azimuth_spinbox.setToolTip(QCoreApplication.translate("polarization", u"The azimuth of incidence.", None))
#endif // QT_CONFIG(tooltip)
        self.azimuth_spinbox.setSuffix(QCoreApplication.translate("polarization", u"\u00b0", None))
#if QT_CONFIG(tooltip)
        self.ak_label.setToolTip(QCoreApplication.translate("polarization", u"\u03a8", None))
#endif // QT_CONFIG(tooltip)
        self.ak_label.setText(QCoreApplication.translate("polarization", u"Factor:", None))
        self.ak_combobox.setItemText(0, QCoreApplication.translate("polarization", u"|Psi|\u00b2", None))
        self.ak_combobox.setItemText(1, QCoreApplication.translate("polarization", u"|A.k|\u00b2", None))
        self.ak_combobox.setItemText(2, QCoreApplication.translate("polarization", u"|A.k|\u00b2 x |Psi|\u00b2 ", None))

#if QT_CONFIG(tooltip)
        self.ak_combobox.setToolTip(QCoreApplication.translate("polarization", u"|Psi|^2 used to be 'no |A.k|^2'\n"
"|A.k|^2 displays only the polarisation factor\n"
"|A.k|^2 x |Psi|^2 displays for all other cases.\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.ak_combobox.setCurrentText(QCoreApplication.translate("polarization", u"|Psi|\u00b2", None))
        self.angle_label.setText(QCoreApplication.translate("polarization", u"Angle of Inc.:", None))
        self.azimuth_label.setText(QCoreApplication.translate("polarization", u"Azimuth of Inc.:", None))
        self.s_share_label.setText(QCoreApplication.translate("polarization", u"s-pol.", None))
#if QT_CONFIG(tooltip)
        self.s_share_spinbox.setToolTip(QCoreApplication.translate("polarization", u"The share of s-polarised light.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

