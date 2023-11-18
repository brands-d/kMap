# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileeditortab.ui'
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

class Ui_fileeditortab(object):
    def setupUi(self, fileeditortab):
        if not fileeditortab.objectName():
            fileeditortab.setObjectName(u"fileeditortab")
        fileeditortab.resize(1018, 733)
        self.verticalLayout = QVBoxLayout(fileeditortab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_layout = QHBoxLayout()
        self.title_layout.setObjectName(u"title_layout")
        self.title_line_edit = QLabel(fileeditortab)
        self.title_line_edit.setObjectName(u"title_line_edit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_line_edit.sizePolicy().hasHeightForWidth())
        self.title_line_edit.setSizePolicy(sizePolicy)

        self.title_layout.addWidget(self.title_line_edit)

        self.reload_button = QPushButton(fileeditortab)
        self.reload_button.setObjectName(u"reload_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.reload_button.sizePolicy().hasHeightForWidth())
        self.reload_button.setSizePolicy(sizePolicy1)

        self.title_layout.addWidget(self.reload_button)

        self.save_button = QPushButton(fileeditortab)
        self.save_button.setObjectName(u"save_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy2)

        self.title_layout.addWidget(self.save_button)


        self.verticalLayout.addLayout(self.title_layout)

        self.display = QTextBrowser(fileeditortab)
        self.display.setObjectName(u"display")
        self.display.setUndoRedoEnabled(False)
        self.display.setReadOnly(False)
        self.display.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextEditable|Qt.TextEditorInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.display.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.display)

        self.search_layout = QHBoxLayout()
        self.search_layout.setObjectName(u"search_layout")
        self.line_edit = QLineEdit(fileeditortab)
        self.line_edit.setObjectName(u"line_edit")
        self.line_edit.setDragEnabled(True)
        self.line_edit.setClearButtonEnabled(True)

        self.search_layout.addWidget(self.line_edit)

        self.find_next_button = QPushButton(fileeditortab)
        self.find_next_button.setObjectName(u"find_next_button")

        self.search_layout.addWidget(self.find_next_button)

        self.find_prev_button = QPushButton(fileeditortab)
        self.find_prev_button.setObjectName(u"find_prev_button")

        self.search_layout.addWidget(self.find_prev_button)


        self.verticalLayout.addLayout(self.search_layout)


        self.retranslateUi(fileeditortab)

        QMetaObject.connectSlotsByName(fileeditortab)
    # setupUi

    def retranslateUi(self, fileeditortab):
        fileeditortab.setWindowTitle(QCoreApplication.translate("fileeditortab", u"Form", None))
        self.title_line_edit.setText(QCoreApplication.translate("fileeditortab", u"Path: ", None))
        self.reload_button.setText(QCoreApplication.translate("fileeditortab", u"Reload", None))
        self.save_button.setText(QCoreApplication.translate("fileeditortab", u"Save", None))
#if QT_CONFIG(shortcut)
        self.save_button.setShortcut(QCoreApplication.translate("fileeditortab", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.display.setHtml(QCoreApplication.translate("fileeditortab", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.line_edit.setPlaceholderText(QCoreApplication.translate("fileeditortab", u"Enter search term here...", None))
        self.find_next_button.setText(QCoreApplication.translate("fileeditortab", u"Find", None))
        self.find_prev_button.setText(QCoreApplication.translate("fileeditortab", u"Find Prev", None))
    # retranslateUi

