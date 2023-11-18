# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitorbitaloptions.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_lmfitother(object):
    def setupUi(self, lmfitother):
        if not lmfitother.objectName():
            lmfitother.setObjectName(u"lmfitother")
        lmfitother.resize(514, 146)
        self.horizontalLayout = QHBoxLayout(lmfitother)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.group_box = QGroupBox(lmfitother)
        self.group_box.setObjectName(u"group_box")
        font = QFont()
        font.setBold(True)
        self.group_box.setFont(font)
        self.group_box.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.group_box)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.symmetrize_combobox = QComboBox(self.group_box)
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
        font1 = QFont()
        font1.setBold(False)
        self.symmetrize_combobox.setFont(font1)
        self.symmetrize_combobox.setMaxVisibleItems(7)
        self.symmetrize_combobox.setMaxCount(7)

        self.gridLayout.addWidget(self.symmetrize_combobox, 3, 1, 1, 1)

        self.polarization_label = QLabel(self.group_box)
        self.polarization_label.setObjectName(u"polarization_label")
        self.polarization_label.setFont(font1)

        self.gridLayout.addWidget(self.polarization_label, 1, 0, 1, 1)

        self.symmetrize_label = QLabel(self.group_box)
        self.symmetrize_label.setObjectName(u"symmetrize_label")
        self.symmetrize_label.setFont(font1)

        self.gridLayout.addWidget(self.symmetrize_label, 3, 0, 1, 1)

        self.ak_combobox = QComboBox(self.group_box)
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

        self.polarization_combobox = QComboBox(self.group_box)
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.setObjectName(u"polarization_combobox")
        sizePolicy.setHeightForWidth(self.polarization_combobox.sizePolicy().hasHeightForWidth())
        self.polarization_combobox.setSizePolicy(sizePolicy)
        self.polarization_combobox.setFont(font1)

        self.gridLayout.addWidget(self.polarization_combobox, 1, 1, 1, 1)

        self.ak_label = QLabel(self.group_box)
        self.ak_label.setObjectName(u"ak_label")
        self.ak_label.setEnabled(True)
        self.ak_label.setFont(font1)

        self.gridLayout.addWidget(self.ak_label, 0, 0, 1, 1)

        self.s_share_label = QLabel(self.group_box)
        self.s_share_label.setObjectName(u"s_share_label")
        self.s_share_label.setFont(font1)

        self.gridLayout.addWidget(self.s_share_label, 2, 0, 1, 1)

        self.s_share_spinbox = QDoubleSpinBox(self.group_box)
        self.s_share_spinbox.setObjectName(u"s_share_spinbox")
        self.s_share_spinbox.setFont(font1)
        self.s_share_spinbox.setKeyboardTracking(False)
        self.s_share_spinbox.setDecimals(3)
        self.s_share_spinbox.setMinimum(0.000000000000000)
        self.s_share_spinbox.setMaximum(1.000000000000000)
        self.s_share_spinbox.setMinimum(0.000000000000000)
        self.s_share_spinbox.setSingleStep(0.010000000000000)
        self.s_share_spinbox.setValue(0.694000000000000)

        self.gridLayout.addWidget(self.s_share_spinbox, 2, 1, 1, 1)


        self.horizontalLayout.addWidget(self.group_box)


        self.retranslateUi(lmfitother)

        self.symmetrize_combobox.setCurrentIndex(0)
        self.ak_combobox.setCurrentIndex(0)
        self.polarization_combobox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(lmfitother)
    # setupUi

    def retranslateUi(self, lmfitother):
        lmfitother.setWindowTitle(QCoreApplication.translate("lmfitother", u"Form", None))
        self.group_box.setTitle(QCoreApplication.translate("lmfitother", u"Orbital Options", None))
        self.symmetrize_combobox.setItemText(0, QCoreApplication.translate("lmfitother", u"No Symmetry", None))
        self.symmetrize_combobox.setItemText(1, QCoreApplication.translate("lmfitother", u"2-Fold", None))
        self.symmetrize_combobox.setItemText(2, QCoreApplication.translate("lmfitother", u"2-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(3, QCoreApplication.translate("lmfitother", u"3-Fold", None))
        self.symmetrize_combobox.setItemText(4, QCoreApplication.translate("lmfitother", u"3-Fold + Mirror", None))
        self.symmetrize_combobox.setItemText(5, QCoreApplication.translate("lmfitother", u"4-Fold", None))
        self.symmetrize_combobox.setItemText(6, QCoreApplication.translate("lmfitother", u"4-Fold + Mirror", None))

        self.polarization_label.setText(QCoreApplication.translate("lmfitother", u"Polarization:", None))
        self.symmetrize_label.setText(QCoreApplication.translate("lmfitother", u"Symmetrization:", None))
        self.ak_combobox.setItemText(0, QCoreApplication.translate("lmfitother", u"|Psi|\u00b2", None))
        self.ak_combobox.setItemText(1, QCoreApplication.translate("lmfitother", u"|A.k|\u00b2", None))
        self.ak_combobox.setItemText(2, QCoreApplication.translate("lmfitother", u"|A.k|\u00b2 x |Psi|\u00b2 ", None))

#if QT_CONFIG(tooltip)
        self.ak_combobox.setToolTip(QCoreApplication.translate("lmfitother", u"|Psi|^2 used to be 'no |A.k|^2'\n"
"|A.k|^2 displays only the polarisation factor\n"
"|A.k|^2 x |Psi|^2 displays for all other cases.\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.ak_combobox.setCurrentText(QCoreApplication.translate("lmfitother", u"|Psi|\u00b2", None))
        self.polarization_combobox.setItemText(0, QCoreApplication.translate("lmfitother", u"Toroid (p-pol)", None))
        self.polarization_combobox.setItemText(1, QCoreApplication.translate("lmfitother", u"p-polarized", None))
        self.polarization_combobox.setItemText(2, QCoreApplication.translate("lmfitother", u"s-polarized", None))
        self.polarization_combobox.setItemText(3, QCoreApplication.translate("lmfitother", u"unpolarized", None))
        self.polarization_combobox.setItemText(4, QCoreApplication.translate("lmfitother", u"circular+", None))
        self.polarization_combobox.setItemText(5, QCoreApplication.translate("lmfitother", u"circular-", None))
        self.polarization_combobox.setItemText(6, QCoreApplication.translate("lmfitother", u"CDAD", None))

#if QT_CONFIG(tooltip)
        self.polarization_combobox.setToolTip(QCoreApplication.translate("lmfitother", u"Choose one type of polarization.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ak_label.setToolTip(QCoreApplication.translate("lmfitother", u"\u03a8", None))
#endif // QT_CONFIG(tooltip)
        self.ak_label.setText(QCoreApplication.translate("lmfitother", u"Factor:", None))
#if QT_CONFIG(tooltip)
        self.s_share_label.setToolTip(QCoreApplication.translate("lmfitother", u"The share of s-polarised light.", None))
#endif // QT_CONFIG(tooltip)
        self.s_share_label.setText(QCoreApplication.translate("lmfitother", u"s-pol. ", None))
#if QT_CONFIG(tooltip)
        self.s_share_spinbox.setToolTip(QCoreApplication.translate("lmfitother", u"The share of s-polarised light.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

