# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabchoosewindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_tabchoosewindow(object):
    def setupUi(self, tabchoosewindow):
        if not tabchoosewindow.objectName():
            tabchoosewindow.setObjectName(u"tabchoosewindow")
        tabchoosewindow.resize(633, 122)
        self.central_widget = QWidget(tabchoosewindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.layout_2 = QVBoxLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.sliced_label = QLabel(self.central_widget)
        self.sliced_label.setObjectName(u"sliced_label")

        self.layout_2.addWidget(self.sliced_label)

        self.sliced_combobox = QComboBox(self.central_widget)
        self.sliced_combobox.setObjectName(u"sliced_combobox")

        self.layout_2.addWidget(self.sliced_combobox)


        self.layout.addLayout(self.layout_2)

        self.layout_3 = QVBoxLayout()
        self.layout_3.setObjectName(u"layout_3")
        self.orbital_label = QLabel(self.central_widget)
        self.orbital_label.setObjectName(u"orbital_label")

        self.layout_3.addWidget(self.orbital_label)

        self.orbital_combobox = QComboBox(self.central_widget)
        self.orbital_combobox.setObjectName(u"orbital_combobox")

        self.layout_3.addWidget(self.orbital_combobox)


        self.layout.addLayout(self.layout_3)


        self.verticalLayout_2.addLayout(self.layout)

        self.layout_4 = QHBoxLayout()
        self.layout_4.setObjectName(u"layout_4")
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_4.addItem(self.spacer)

        self.load = QPushButton(self.central_widget)
        self.load.setObjectName(u"load")

        self.layout_4.addWidget(self.load)


        self.verticalLayout_2.addLayout(self.layout_4)

        tabchoosewindow.setCentralWidget(self.central_widget)

        self.retranslateUi(tabchoosewindow)

        QMetaObject.connectSlotsByName(tabchoosewindow)
    # setupUi

    def retranslateUi(self, tabchoosewindow):
        tabchoosewindow.setWindowTitle(QCoreApplication.translate("tabchoosewindow", u"Choose Tabs...", None))
        self.sliced_label.setText(QCoreApplication.translate("tabchoosewindow", u"Choose a SlicedData Tab", None))
        self.orbital_label.setText(QCoreApplication.translate("tabchoosewindow", u"Choose an OrbitalData Tab", None))
        self.load.setText(QCoreApplication.translate("tabchoosewindow", u"Load", None))
    # retranslateUi

