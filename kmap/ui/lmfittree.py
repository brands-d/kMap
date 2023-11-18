# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfittree.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_lmfittree(object):
    def setupUi(self, lmfittree):
        if not lmfittree.objectName():
            lmfittree.setObjectName(u"lmfittree")
        lmfittree.resize(889, 422)
        self.horizontalLayout = QHBoxLayout(lmfittree)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tree = QTreeWidget(lmfittree)
        self.tree.setObjectName(u"tree")
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setAlternatingRowColors(True)
        self.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tree.setColumnCount(8)
        self.tree.header().setMinimumSectionSize(10)
        self.tree.header().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.tree)


        self.retranslateUi(lmfittree)

        QMetaObject.connectSlotsByName(lmfittree)
    # setupUi

    def retranslateUi(self, lmfittree):
        lmfittree.setWindowTitle(QCoreApplication.translate("lmfittree", u"Form", None))
        ___qtreewidgetitem = self.tree.headerItem()
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("lmfittree", u"Expression", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("lmfittree", u"Max", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("lmfittree", u"Min", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("lmfittree", u"Initial", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("lmfittree", u"Vary", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("lmfittree", u"Alias", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("lmfittree", u"Parameter", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("lmfittree", u"ID", None));
    # retranslateUi

