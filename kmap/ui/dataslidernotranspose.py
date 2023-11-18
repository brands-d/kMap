# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataslidernotranspose.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSlider,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_dataslider(object):
    def setupUi(self, dataslider):
        if not dataslider.objectName():
            dataslider.setObjectName(u"dataslider")
        dataslider.resize(535, 220)
        self.horizontalLayout_3 = QHBoxLayout(dataslider)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupbox = QGroupBox(dataslider)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.groupbox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.combobox = QComboBox(self.groupbox)
        self.combobox.setObjectName(u"combobox")
        font1 = QFont()
        font1.setBold(False)
        self.combobox.setFont(font1)
        self.combobox.setMaxVisibleItems(3)
        self.combobox.setMaxCount(3)
        self.combobox.setDuplicatesEnabled(True)

        self.layout.addWidget(self.combobox)

        self.value_label = QLabel(self.groupbox)
        self.value_label.setObjectName(u"value_label")
        self.value_label.setFont(font1)
        self.value_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout.addWidget(self.value_label)

        self.layout.setStretch(0, 5)
        self.layout.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.layout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slider = QSlider(self.groupbox)
        self.slider.setObjectName(u"slider")
        self.slider.setFont(font1)
        self.slider.setMaximum(0)
        self.slider.setSliderPosition(0)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(0)

        self.horizontalLayout.addWidget(self.slider)

        self.spinbox = QSpinBox(self.groupbox)
        self.spinbox.setObjectName(u"spinbox")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox.sizePolicy().hasHeightForWidth())
        self.spinbox.setSizePolicy(sizePolicy)
        self.spinbox.setMinimumSize(QSize(70, 0))
        self.spinbox.setMaximumSize(QSize(70, 16777215))
        self.spinbox.setFont(font1)
        self.spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.spinbox.setKeyboardTracking(False)
        self.spinbox.setMaximum(0)
        self.spinbox.setValue(0)

        self.horizontalLayout.addWidget(self.spinbox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.symmetrize_label = QLabel(self.groupbox)
        self.symmetrize_label.setObjectName(u"symmetrize_label")
        self.symmetrize_label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.symmetrize_label)

        self.symmetrize_combobox = QComboBox(self.groupbox)
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.setObjectName(u"symmetrize_combobox")
        self.symmetrize_combobox.setFont(font1)

        self.horizontalLayout_2.addWidget(self.symmetrize_combobox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addWidget(self.groupbox)


        self.retranslateUi(dataslider)

        QMetaObject.connectSlotsByName(dataslider)
    # setupUi

    def retranslateUi(self, dataslider):
        dataslider.setWindowTitle(QCoreApplication.translate("dataslider", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("dataslider", u"Data Slices", None))
#if QT_CONFIG(tooltip)
        self.value_label.setToolTip(QCoreApplication.translate("dataslider", u"Slice key of the current slice.", None))
#endif // QT_CONFIG(tooltip)
        self.value_label.setText("")
#if QT_CONFIG(tooltip)
        self.slider.setToolTip(QCoreApplication.translate("dataslider", u"Drag the slider to change the displayed slice of data.", None))
#endif // QT_CONFIG(tooltip)
        self.symmetrize_label.setText(QCoreApplication.translate("dataslider", u"Symmetrization:", None))
        self.symmetrize_combobox.setItemText(0, QCoreApplication.translate("dataslider", u"No Symmetry", None))
        self.symmetrize_combobox.setItemText(1, QCoreApplication.translate("dataslider", u"2-Fold", None))
        self.symmetrize_combobox.setItemText(2, QCoreApplication.translate("dataslider", u"2-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(3, QCoreApplication.translate("dataslider", u"3-Fold", None))
        self.symmetrize_combobox.setItemText(4, QCoreApplication.translate("dataslider", u"3-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(5, QCoreApplication.translate("dataslider", u"4-Fold", None))
        self.symmetrize_combobox.setItemText(6, QCoreApplication.translate("dataslider", u"4-Fold + Mirror", None))

    # retranslateUi

