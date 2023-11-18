# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitresulttree.ui'
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

class Ui_lmfitresulttree(object):
    def setupUi(self, lmfitresulttree):
        if not lmfitresulttree.objectName():
            lmfitresulttree.setObjectName(u"lmfitresulttree")
        lmfitresulttree.resize(1353, 706)
        self.horizontalLayout = QHBoxLayout(lmfitresulttree)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, 0, 0)
        self.tree = QTreeWidget(lmfitresulttree)
        self.tree.setObjectName(u"tree")
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setAlternatingRowColors(True)
        self.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tree.setColumnCount(5)
        self.tree.header().setMinimumSectionSize(10)
        self.tree.header().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.tree)


        self.retranslateUi(lmfitresulttree)

        QMetaObject.connectSlotsByName(lmfitresulttree)
    # setupUi

    def retranslateUi(self, lmfitresulttree):
        lmfitresulttree.setWindowTitle(QCoreApplication.translate("lmfitresulttree", u"Form", None))
        ___qtreewidgetitem = self.tree.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("lmfitresulttree", u"Uncertainty", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("lmfitresulttree", u"Result", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("lmfitresulttree", u"Alias", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("lmfitresulttree", u"Parameter", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("lmfitresulttree", u"ID", None));
    # retranslateUi

