# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splitviewoptions.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_cubeoptions(object):
    def setupUi(self, cubeoptions):
        if not cubeoptions.objectName():
            cubeoptions.setObjectName(u"cubeoptions")
        cubeoptions.resize(472, 70)
        self.horizontalLayout = QHBoxLayout(cubeoptions)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.groupbox = QGroupBox(cubeoptions)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_2 = QHBoxLayout(self.groupbox)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.type_label = QLabel(self.groupbox)
        self.type_label.setObjectName(u"type_label")
        font1 = QFont()
        font1.setBold(False)
        self.type_label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.type_label)

        self.type_combobox = QComboBox(self.groupbox)
        self.type_combobox.addItem("")
        self.type_combobox.addItem("")
        self.type_combobox.addItem("")
        self.type_combobox.addItem("")
        self.type_combobox.setObjectName(u"type_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_combobox.sizePolicy().hasHeightForWidth())
        self.type_combobox.setSizePolicy(sizePolicy)
        self.type_combobox.setFont(font1)
        self.type_combobox.setMaxVisibleItems(7)
        self.type_combobox.setMaxCount(7)

        self.horizontalLayout_2.addWidget(self.type_combobox)

        self.scale_label = QLabel(self.groupbox)
        self.scale_label.setObjectName(u"scale_label")
        self.scale_label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.scale_label)

        self.scale_spinbox = QDoubleSpinBox(self.groupbox)
        self.scale_spinbox.setObjectName(u"scale_spinbox")
        self.scale_spinbox.setFont(font1)
        self.scale_spinbox.setAlignment(Qt.AlignCenter)
        self.scale_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.scale_spinbox.setKeyboardTracking(False)
        self.scale_spinbox.setDecimals(3)
        self.scale_spinbox.setMinimum(0.000000000000000)
        self.scale_spinbox.setMaximum(9999999.000000000000000)
        self.scale_spinbox.setSingleStep(1.000000000000000)
        self.scale_spinbox.setValue(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.scale_spinbox)


        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(cubeoptions)

        self.type_combobox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(cubeoptions)
    # setupUi

    def retranslateUi(self, cubeoptions):
        cubeoptions.setWindowTitle(QCoreApplication.translate("cubeoptions", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("cubeoptions", u"Split View Options", None))
        self.type_label.setText(QCoreApplication.translate("cubeoptions", u"Split Type", None))
        self.type_combobox.setItemText(0, QCoreApplication.translate("cubeoptions", u"Left Right", None))
        self.type_combobox.setItemText(1, QCoreApplication.translate("cubeoptions", u"Right Left", None))
        self.type_combobox.setItemText(2, QCoreApplication.translate("cubeoptions", u"Top Bottom", None))
        self.type_combobox.setItemText(3, QCoreApplication.translate("cubeoptions", u"Bottom Top", None))

#if QT_CONFIG(tooltip)
        self.type_combobox.setToolTip(QCoreApplication.translate("cubeoptions", u"Way of splitting the images.\n"
"", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.scale_label.setToolTip(QCoreApplication.translate("cubeoptions", u"Scaling factor for the orbital data.", None))
#endif // QT_CONFIG(tooltip)
        self.scale_label.setText(QCoreApplication.translate("cubeoptions", u"Scaling:", None))
        self.scale_spinbox.setSuffix("")
    # retranslateUi

