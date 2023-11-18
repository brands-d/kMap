# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileviewertab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_fileviewertab(object):
    def setupUi(self, fileviewertab):
        if not fileviewertab.objectName():
            fileviewertab.setObjectName(u"fileviewertab")
        fileviewertab.resize(1073, 611)
        self.verticalLayout = QVBoxLayout(fileviewertab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_layout = QHBoxLayout()
        self.title_layout.setObjectName(u"title_layout")
        self.title_line_edit = QLabel(fileviewertab)
        self.title_line_edit.setObjectName(u"title_line_edit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_line_edit.sizePolicy().hasHeightForWidth())
        self.title_line_edit.setSizePolicy(sizePolicy)

        self.title_layout.addWidget(self.title_line_edit)

        self.reload_button = QPushButton(fileviewertab)
        self.reload_button.setObjectName(u"reload_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.reload_button.sizePolicy().hasHeightForWidth())
        self.reload_button.setSizePolicy(sizePolicy1)

        self.title_layout.addWidget(self.reload_button)


        self.verticalLayout.addLayout(self.title_layout)

        self.display = QTextBrowser(fileviewertab)
        self.display.setObjectName(u"display")
        self.display.setUndoRedoEnabled(False)
        self.display.setReadOnly(True)
        self.display.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.display.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.display)

        self.search_layout = QHBoxLayout()
        self.search_layout.setObjectName(u"search_layout")
        self.line_edit = QLineEdit(fileviewertab)
        self.line_edit.setObjectName(u"line_edit")
        self.line_edit.setDragEnabled(True)
        self.line_edit.setClearButtonEnabled(True)

        self.search_layout.addWidget(self.line_edit)

        self.find_next_button = QPushButton(fileviewertab)
        self.find_next_button.setObjectName(u"find_next_button")

        self.search_layout.addWidget(self.find_next_button)

        self.find_prev_button = QPushButton(fileviewertab)
        self.find_prev_button.setObjectName(u"find_prev_button")

        self.search_layout.addWidget(self.find_prev_button)


        self.verticalLayout.addLayout(self.search_layout)


        self.retranslateUi(fileviewertab)

        QMetaObject.connectSlotsByName(fileviewertab)
    # setupUi

    def retranslateUi(self, fileviewertab):
        fileviewertab.setWindowTitle(QCoreApplication.translate("fileviewertab", u"Form", None))
        self.title_line_edit.setText(QCoreApplication.translate("fileviewertab", u"Path: ", None))
        self.reload_button.setText(QCoreApplication.translate("fileviewertab", u"Reload", None))
        self.display.setHtml(QCoreApplication.translate("fileviewertab", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.line_edit.setPlaceholderText(QCoreApplication.translate("fileviewertab", u"Enter search term here...", None))
        self.find_next_button.setText(QCoreApplication.translate("fileviewertab", u"Find", None))
        self.find_prev_button.setText(QCoreApplication.translate("fileviewertab", u"Find Prev", None))
    # retranslateUi

