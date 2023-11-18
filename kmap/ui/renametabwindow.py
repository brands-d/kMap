# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'renametabwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLineEdit,
    QMainWindow, QSizePolicy, QWidget)

class Ui_rename_tab(object):
    def setupUi(self, rename_tab):
        if not rename_tab.objectName():
            rename_tab.setObjectName(u"rename_tab")
        rename_tab.resize(635, 89)
        self.central_widget = QWidget(rename_tab)
        self.central_widget.setObjectName(u"central_widget")
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name_groupbox = QGroupBox(self.central_widget)
        self.name_groupbox.setObjectName(u"name_groupbox")
        font = QFont()
        font.setBold(True)
        self.name_groupbox.setFont(font)
        self.name_groupbox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_3 = QHBoxLayout(self.name_groupbox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.rename_tab_edit = QLineEdit(self.name_groupbox)
        self.rename_tab_edit.setObjectName(u"rename_tab_edit")
        font1 = QFont()
        font1.setBold(False)
        self.rename_tab_edit.setFont(font1)
        self.rename_tab_edit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.rename_tab_edit)


        self.horizontalLayout.addWidget(self.name_groupbox)

        rename_tab.setCentralWidget(self.central_widget)

        self.retranslateUi(rename_tab)

        QMetaObject.connectSlotsByName(rename_tab)
    # setupUi

    def retranslateUi(self, rename_tab):
        rename_tab.setWindowTitle(QCoreApplication.translate("rename_tab", u"MainWindow", None))
        self.name_groupbox.setTitle(QCoreApplication.translate("rename_tab", u"Rename Tab", None))
        self.rename_tab_edit.setPlaceholderText(QCoreApplication.translate("rename_tab", u"Enter new name here...", None))
    # retranslateUi

