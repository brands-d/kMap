# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cubeoptions.ui'
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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_cubeoptions(object):
    def setupUi(self, cubeoptions):
        if not cubeoptions.objectName():
            cubeoptions.setObjectName(u"cubeoptions")
        cubeoptions.resize(359, 187)
        self.horizontalLayout = QHBoxLayout(cubeoptions)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.groupbox = QGroupBox(cubeoptions)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.groupbox)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 15, 5, 0)
        self.energy_label = QLabel(self.groupbox)
        self.energy_label.setObjectName(u"energy_label")
        font1 = QFont()
        font1.setBold(False)
        self.energy_label.setFont(font1)

        self.gridLayout.addWidget(self.energy_label, 0, 0, 1, 1)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.energy_spinbox = QDoubleSpinBox(self.groupbox)
        self.energy_spinbox.setObjectName(u"energy_spinbox")
        self.energy_spinbox.setFont(font1)
        self.energy_spinbox.setAlignment(Qt.AlignCenter)
        self.energy_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.energy_spinbox.setKeyboardTracking(False)
        self.energy_spinbox.setDecimals(1)
        self.energy_spinbox.setMinimum(5.000000000000000)
        self.energy_spinbox.setMaximum(150.000000000000000)
        self.energy_spinbox.setSingleStep(1.000000000000000)
        self.energy_spinbox.setValue(30.000000000000000)

        self.layout.addWidget(self.energy_spinbox)

        self.match_button = QPushButton(self.groupbox)
        self.match_button.setObjectName(u"match_button")
        self.match_button.setFont(font1)

        self.layout.addWidget(self.match_button)


        self.gridLayout.addLayout(self.layout, 0, 1, 1, 1)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.spacer, 4, 0, 1, 1)

        self.symmetrize_label = QLabel(self.groupbox)
        self.symmetrize_label.setObjectName(u"symmetrize_label")
        self.symmetrize_label.setFont(font1)

        self.gridLayout.addWidget(self.symmetrize_label, 2, 0, 1, 1)

        self.resolution_spinbox = QDoubleSpinBox(self.groupbox)
        self.resolution_spinbox.setObjectName(u"resolution_spinbox")
        self.resolution_spinbox.setFont(font1)
        self.resolution_spinbox.setAlignment(Qt.AlignCenter)
        self.resolution_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.resolution_spinbox.setKeyboardTracking(False)
        self.resolution_spinbox.setDecimals(3)
        self.resolution_spinbox.setMinimum(0.010000000000000)
        self.resolution_spinbox.setMaximum(0.100000000000000)
        self.resolution_spinbox.setSingleStep(0.001000000000000)
        self.resolution_spinbox.setValue(0.030000000000000)

        self.gridLayout.addWidget(self.resolution_spinbox, 1, 1, 1, 1)

        self.symmetrize_combobox = QComboBox(self.groupbox)
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.addItem("")
        self.symmetrize_combobox.setObjectName(u"symmetrize_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.symmetrize_combobox.sizePolicy().hasHeightForWidth())
        self.symmetrize_combobox.setSizePolicy(sizePolicy)
        self.symmetrize_combobox.setFont(font1)
        self.symmetrize_combobox.setMaxVisibleItems(7)
        self.symmetrize_combobox.setMaxCount(7)

        self.gridLayout.addWidget(self.symmetrize_combobox, 2, 1, 1, 1)

        self.resolution_label = QLabel(self.groupbox)
        self.resolution_label.setObjectName(u"resolution_label")
        self.resolution_label.setFont(font1)

        self.gridLayout.addWidget(self.resolution_label, 1, 0, 1, 1)

        self.inner_potential_label = QLabel(self.groupbox)
        self.inner_potential_label.setObjectName(u"inner_potential_label")
        self.inner_potential_label.setFont(font1)

        self.gridLayout.addWidget(self.inner_potential_label, 3, 0, 1, 1)

        self.inner_potential_spinbox = QDoubleSpinBox(self.groupbox)
        self.inner_potential_spinbox.setObjectName(u"inner_potential_spinbox")
        self.inner_potential_spinbox.setFont(font1)
        self.inner_potential_spinbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.inner_potential_spinbox.setDecimals(1)
        self.inner_potential_spinbox.setMaximum(30.000000000000000)

        self.gridLayout.addWidget(self.inner_potential_spinbox, 3, 1, 1, 1)


        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(cubeoptions)

        self.symmetrize_combobox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(cubeoptions)
    # setupUi

    def retranslateUi(self, cubeoptions):
        cubeoptions.setWindowTitle(QCoreApplication.translate("cubeoptions", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("cubeoptions", u"Cube Options", None))
        self.energy_label.setText(QCoreApplication.translate("cubeoptions", u"Kinetic Energy:", None))
        self.energy_spinbox.setSuffix(QCoreApplication.translate("cubeoptions", u"  eV", None))
#if QT_CONFIG(tooltip)
        self.match_button.setToolTip(QCoreApplication.translate("cubeoptions", u"Matches the kinetic energy value with the average,\n"
"the max, the min or the current value of the slice\n"
"axis of the first SlicedDataTab open.\n"
"\n"
"See general settings ([orbital]) to change the \n"
"behaviour.", None))
#endif // QT_CONFIG(tooltip)
        self.match_button.setText(QCoreApplication.translate("cubeoptions", u"Match", None))
        self.symmetrize_label.setText(QCoreApplication.translate("cubeoptions", u"Symmetrization:", None))
        self.resolution_spinbox.setSuffix(QCoreApplication.translate("cubeoptions", u"  \u212b^-1", None))
        self.symmetrize_combobox.setItemText(0, QCoreApplication.translate("cubeoptions", u"No Symmetry", None))
        self.symmetrize_combobox.setItemText(1, QCoreApplication.translate("cubeoptions", u"2-Fold", None))
        self.symmetrize_combobox.setItemText(2, QCoreApplication.translate("cubeoptions", u"2-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(3, QCoreApplication.translate("cubeoptions", u"3-Fold", None))
        self.symmetrize_combobox.setItemText(4, QCoreApplication.translate("cubeoptions", u"3-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(5, QCoreApplication.translate("cubeoptions", u"4-Fold", None))
        self.symmetrize_combobox.setItemText(6, QCoreApplication.translate("cubeoptions", u"4-Fold + Mirror", None))

        self.resolution_label.setText(QCoreApplication.translate("cubeoptions", u"Resolution:", None))
        self.inner_potential_label.setText(QCoreApplication.translate("cubeoptions", u"Inner Potential:", None))
        self.inner_potential_spinbox.setSuffix(QCoreApplication.translate("cubeoptions", u" eV", None))
    # retranslateUi

