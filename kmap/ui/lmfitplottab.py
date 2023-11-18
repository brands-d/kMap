# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitplottab.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from kmap.controller.lmfitplot import LMFitPlot

class Ui_lmfitplottab(object):
    def setupUi(self, lmfitplottab):
        if not lmfitplottab.objectName():
            lmfitplottab.setObjectName(u"lmfitplottab")
        lmfitplottab.resize(1213, 927)
        self.horizontalLayout = QHBoxLayout(lmfitplottab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scroll_area = QScrollArea(lmfitplottab)
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
        self.parameter_groupbox = QGroupBox(self.scrollAreaWidgetContents)
        self.parameter_groupbox.setObjectName(u"parameter_groupbox")
        font = QFont()
        font.setBold(True)
        self.parameter_groupbox.setFont(font)
        self.parameter_groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_4 = QVBoxLayout(self.parameter_groupbox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.parameter_combobox = QComboBox(self.parameter_groupbox)
        self.parameter_combobox.addItem("")
        self.parameter_combobox.addItem("")
        self.parameter_combobox.addItem("")
        self.parameter_combobox.addItem("")
        self.parameter_combobox.addItem("")
        self.parameter_combobox.setObjectName(u"parameter_combobox")
        font1 = QFont()
        font1.setBold(False)
        self.parameter_combobox.setFont(font1)
        self.parameter_combobox.setInsertPolicy(QComboBox.InsertAtBottom)

        self.verticalLayout_4.addWidget(self.parameter_combobox)


        self.verticalLayout.addWidget(self.parameter_groupbox)

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
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.refresh_button = QPushButton(self.options_groupbox)
        self.refresh_button.setObjectName(u"refresh_button")
        self.refresh_button.setFont(font1)

        self.verticalLayout_2.addWidget(self.refresh_button)


        self.verticalLayout.addWidget(self.options_groupbox)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacer)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scroll_area)

        self.plot_item = LMFitPlot(lmfitplottab)
        self.plot_item.setObjectName(u"plot_item")

        self.horizontalLayout.addWidget(self.plot_item)


        self.retranslateUi(lmfitplottab)

        QMetaObject.connectSlotsByName(lmfitplottab)
    # setupUi

    def retranslateUi(self, lmfitplottab):
        lmfitplottab.setWindowTitle(QCoreApplication.translate("lmfitplottab", u"Form", None))
        self.parameter_groupbox.setTitle(QCoreApplication.translate("lmfitplottab", u"Plot Types", None))
        self.parameter_combobox.setItemText(0, QCoreApplication.translate("lmfitplottab", u"Weight", None))
        self.parameter_combobox.setItemText(1, QCoreApplication.translate("lmfitplottab", u"Phi", None))
        self.parameter_combobox.setItemText(2, QCoreApplication.translate("lmfitplottab", u"Theta", None))
        self.parameter_combobox.setItemText(3, QCoreApplication.translate("lmfitplottab", u"Psi", None))
        self.parameter_combobox.setItemText(4, QCoreApplication.translate("lmfitplottab", u"Residual", None))

        self.options_groupbox.setTitle(QCoreApplication.translate("lmfitplottab", u"Options", None))
        self.refresh_button.setText(QCoreApplication.translate("lmfitplottab", u"Refresh Plot", None))
    # retranslateUi

