# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splitviewtab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from kmap.controller.pyqtgraphplot import PyQtGraphPlot

class Ui_splitviewtab(object):
    def setupUi(self, splitviewtab):
        if not splitviewtab.objectName():
            splitviewtab.setObjectName(u"splitviewtab")
        splitviewtab.resize(1823, 809)
        self.horizontalLayout = QHBoxLayout(splitviewtab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(splitviewtab)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setMinimumSize(QSize(625, 0))
        self.scroll_area.setMaximumSize(QSize(625, 16777215))
        self.scroll_area.setWidgetResizable(True)
        self.layout = QWidget()
        self.layout.setObjectName(u"layout")
        self.layout.setGeometry(QRect(0, 0, 623, 797))
        self.verticalLayout = QVBoxLayout(self.layout)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 1, 1, 1)
        self.spacer = QSpacerItem(20, 739, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacer)

        self.scroll_area.setWidget(self.layout)

        self.horizontalLayout.addWidget(self.scroll_area)

        self.plot_item = PyQtGraphPlot(splitviewtab)
        self.plot_item.setObjectName(u"plot_item")

        self.horizontalLayout.addWidget(self.plot_item)


        self.retranslateUi(splitviewtab)

        QMetaObject.connectSlotsByName(splitviewtab)
    # setupUi

    def retranslateUi(self, splitviewtab):
        splitviewtab.setWindowTitle(QCoreApplication.translate("splitviewtab", u"Form", None))
    # retranslateUi

