# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'colormap.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_colormap(object):
    def setupUi(self, colormap):
        if not colormap.objectName():
            colormap.setObjectName(u"colormap")
        colormap.resize(474, 123)
        font = QFont()
        font.setBold(False)
        colormap.setFont(font)
        colormap.setAutoFillBackground(False)
        self.horizontal_layout = QHBoxLayout(colormap)
        self.horizontal_layout.setSpacing(7)
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)
        self.groupbox = QGroupBox(colormap)
        self.groupbox.setObjectName(u"groupbox")
        font1 = QFont()
        font1.setBold(True)
        self.groupbox.setFont(font1)
        self.groupbox.setAlignment(Qt.AlignCenter)
        self.groupbox.setFlat(False)
        self.groupbox.setCheckable(False)
        self.horizontalLayout = QHBoxLayout(self.groupbox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 15, 5, 5)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.combobox = QComboBox(self.groupbox)
        self.combobox.setObjectName(u"combobox")
        self.combobox.setFont(font)

        self.top_layout.addWidget(self.combobox)

        self.remove_button = QPushButton(self.groupbox)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        self.remove_button.setFont(font)

        self.top_layout.addWidget(self.remove_button)

        self.reload_button = QPushButton(self.groupbox)
        self.reload_button.setObjectName(u"reload_button")
        sizePolicy.setHeightForWidth(self.reload_button.sizePolicy().hasHeightForWidth())
        self.reload_button.setSizePolicy(sizePolicy)
        self.reload_button.setFont(font)

        self.top_layout.addWidget(self.reload_button)


        self.vertical_layout.addLayout(self.top_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.line_edit = QLineEdit(self.groupbox)
        self.line_edit.setObjectName(u"line_edit")
        self.line_edit.setFont(font)
        self.line_edit.setDragEnabled(True)
        self.line_edit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.line_edit.setClearButtonEnabled(True)

        self.bottom_layout.addWidget(self.line_edit)

        self.add_button = QPushButton(self.groupbox)
        self.add_button.setObjectName(u"add_button")
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        self.add_button.setFont(font)

        self.bottom_layout.addWidget(self.add_button)

        self.save_button = QPushButton(self.groupbox)
        self.save_button.setObjectName(u"save_button")
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setFont(font)

        self.bottom_layout.addWidget(self.save_button)


        self.vertical_layout.addLayout(self.bottom_layout)


        self.horizontalLayout.addLayout(self.vertical_layout)


        self.horizontal_layout.addWidget(self.groupbox)


        self.retranslateUi(colormap)

        QMetaObject.connectSlotsByName(colormap)
    # setupUi

    def retranslateUi(self, colormap):
        colormap.setWindowTitle(QCoreApplication.translate("colormap", u"Colormap", None))
        self.groupbox.setTitle(QCoreApplication.translate("colormap", u"Colormap", None))
#if QT_CONFIG(tooltip)
        self.combobox.setToolTip(QCoreApplication.translate("colormap", u"Choose a colormap for the connected plot.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.remove_button.setToolTip(QCoreApplication.translate("colormap", u"Removes the current selected colormap from the list of colormaps.\n"
"\n"
"To make this removal permanently(!) click 'Save'.", None))
#endif // QT_CONFIG(tooltip)
        self.remove_button.setText(QCoreApplication.translate("colormap", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.reload_button.setToolTip(QCoreApplication.translate("colormap", u"Reloads the .json file containing the colormaps.\n"
"It will bring back removed colormaps if not saved since then.\n"
"\n"
"This will DELETE unsaved colormaps in the list.", None))
#endif // QT_CONFIG(tooltip)
        self.reload_button.setText(QCoreApplication.translate("colormap", u"Reload", None))
#if QT_CONFIG(tooltip)
        self.line_edit.setToolTip(QCoreApplication.translate("colormap", u"Enter the name for the colormap here.", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit.setPlaceholderText(QCoreApplication.translate("colormap", u"Enter new name...", None))
#if QT_CONFIG(tooltip)
        self.add_button.setToolTip(QCoreApplication.translate("colormap", u"Adds the current colormap from the connected plot to the list of colormaps under the name entered into the line edit.\n"
"\n"
"If it contains no name, nothing will happen.\n"
"\n"
"To save the colormap permanently click 'Save'.", None))
#endif // QT_CONFIG(tooltip)
        self.add_button.setText(QCoreApplication.translate("colormap", u"Add", None))
#if QT_CONFIG(tooltip)
        self.save_button.setToolTip(QCoreApplication.translate("colormap", u"Saves the current list of colormaps permanently to the .json file.", None))
#endif // QT_CONFIG(tooltip)
        self.save_button.setText(QCoreApplication.translate("colormap", u"Save", None))
    # retranslateUi

