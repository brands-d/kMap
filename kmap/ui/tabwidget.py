# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_tabwidget(object):
    def setupUi(self, tabwidget):
        if not tabwidget.objectName():
            tabwidget.setObjectName(u"tabwidget")
        tabwidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(tabwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.tab_widget = QTabWidget(tabwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)

        self.verticalLayout.addWidget(self.tab_widget)


        self.retranslateUi(tabwidget)

        self.tab_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(tabwidget)
    # setupUi

    def retranslateUi(self, tabwidget):
        tabwidget.setWindowTitle(QCoreApplication.translate("tabwidget", u"Form", None))
    # retranslateUi

