# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'orbitaltable.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_orbitaltable(object):
    def setupUi(self, orbitaltable):
        if not orbitaltable.objectName():
            orbitaltable.setObjectName(u"orbitaltable")
        orbitaltable.resize(947, 627)
        self.horizontalLayout = QHBoxLayout(orbitaltable)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.groupbox = QGroupBox(orbitaltable)
        self.groupbox.setObjectName(u"groupbox")
        font = QFont()
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_2 = QHBoxLayout(self.groupbox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 15, 5, 5)
        self.table = QTableWidget(self.groupbox)
        if (self.table.columnCount() < 8):
            self.table.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.table.setObjectName(u"table")
        font1 = QFont()
        font1.setBold(False)
        self.table.setFont(font1)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setProperty("showDropIndicator", False)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setMinimumSectionSize(10)
        self.table.horizontalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.table)


        self.horizontalLayout.addWidget(self.groupbox)


        self.retranslateUi(orbitaltable)

        QMetaObject.connectSlotsByName(orbitaltable)
    # setupUi

    def retranslateUi(self, orbitaltable):
        orbitaltable.setWindowTitle(QCoreApplication.translate("orbitaltable", u"Form", None))
        self.groupbox.setTitle(QCoreApplication.translate("orbitaltable", u"Loaded Orbitals", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("orbitaltable", u"ID", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("orbitaltable", u"Name", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("orbitaltable", u"Weight", None));
        ___qtablewidgetitem3 = self.table.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("orbitaltable", u"Phi", None));
        ___qtablewidgetitem4 = self.table.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("orbitaltable", u"Theta", None));
        ___qtablewidgetitem5 = self.table.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("orbitaltable", u"Psi", None));
        ___qtablewidgetitem6 = self.table.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("orbitaltable", u"Use", None));
    # retranslateUi

