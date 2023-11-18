# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'matplotlibwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy, QWidget)

class Ui_matplotlibwindow(object):
    def setupUi(self, matplotlibwindow):
        if not matplotlibwindow.objectName():
            matplotlibwindow.setObjectName(u"matplotlibwindow")
        matplotlibwindow.resize(500, 550)
        self.central_widget = QWidget(matplotlibwindow)
        self.central_widget.setObjectName(u"central_widget")
        matplotlibwindow.setCentralWidget(self.central_widget)

        self.retranslateUi(matplotlibwindow)

        QMetaObject.connectSlotsByName(matplotlibwindow)
    # setupUi

    def retranslateUi(self, matplotlibwindow):
        matplotlibwindow.setWindowTitle(QCoreApplication.translate("matplotlibwindow", u"Matplotlib", None))
    # retranslateUi

