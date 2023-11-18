# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'databasewindow.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLineEdit, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.setWindowModality(Qt.NonModal)
        main_window.resize(1129, 566)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.database_groupbox = QGroupBox(self.central_widget)
        self.database_groupbox.setObjectName(u"database_groupbox")
        font = QFont()
        font.setBold(True)
        self.database_groupbox.setFont(font)
        self.database_groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.database_groupbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tree = QTreeWidget(self.database_groupbox)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(6, u"7");
        __qtreewidgetitem.setText(5, u"6");
        __qtreewidgetitem.setText(4, u"5");
        __qtreewidgetitem.setText(3, u"4");
        __qtreewidgetitem.setText(2, u"3");
        __qtreewidgetitem.setText(1, u"2");
        __qtreewidgetitem.setText(0, u"1");
        self.tree.setHeaderItem(__qtreewidgetitem)
        self.tree.setObjectName(u"tree")
        font1 = QFont()
        font1.setBold(False)
        self.tree.setFont(font1)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tree.setSortingEnabled(True)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(7)
        self.tree.header().setMinimumSectionSize(10)
        self.tree.header().setDefaultSectionSize(67)
        self.tree.header().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.tree)

        self.database_layout = QHBoxLayout()
        self.database_layout.setObjectName(u"database_layout")
        self.combobox = QComboBox(self.database_groupbox)
        self.combobox.addItem("")
        self.combobox.addItem("")
        self.combobox.addItem("")
        self.combobox.addItem("")
        self.combobox.addItem("")
        self.combobox.setObjectName(u"combobox")
        self.combobox.setMinimumSize(QSize(150, 0))
        self.combobox.setFont(font1)
        self.combobox.setEditable(False)
        self.combobox.setFrame(True)

        self.database_layout.addWidget(self.combobox)

        self.line_edit = QLineEdit(self.database_groupbox)
        self.line_edit.setObjectName(u"line_edit")
        self.line_edit.setMinimumSize(QSize(250, 0))
        self.line_edit.setFont(font1)
        self.line_edit.setClearButtonEnabled(True)

        self.database_layout.addWidget(self.line_edit)

        self.find_button = QPushButton(self.database_groupbox)
        self.find_button.setObjectName(u"find_button")
        self.find_button.setFont(font1)

        self.database_layout.addWidget(self.find_button)

        self.top_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.database_layout.addItem(self.top_spacer)

        self.database_load_button = QPushButton(self.database_groupbox)
        self.database_load_button.setObjectName(u"database_load_button")
        self.database_load_button.setFont(font1)
        self.database_load_button.setAutoDefault(False)

        self.database_layout.addWidget(self.database_load_button)

        self.database_layout.setStretch(0, 1)
        self.database_layout.setStretch(1, 3)
        self.database_layout.setStretch(3, 2)

        self.verticalLayout_3.addLayout(self.database_layout)


        self.verticalLayout.addWidget(self.database_groupbox)

        self.url_groupbox = QGroupBox(self.central_widget)
        self.url_groupbox.setObjectName(u"url_groupbox")
        self.url_groupbox.setFont(font)
        self.url_groupbox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.url_groupbox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.text_edit = QPlainTextEdit(self.url_groupbox)
        self.text_edit.setObjectName(u"text_edit")
        self.text_edit.setFont(font1)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.verticalLayout_2.addWidget(self.text_edit)

        self.url_layout = QHBoxLayout()
        self.url_layout.setObjectName(u"url_layout")
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.url_layout.addItem(self.bottom_spacer)

        self.url_load_button = QPushButton(self.url_groupbox)
        self.url_load_button.setObjectName(u"url_load_button")
        self.url_load_button.setFont(font1)

        self.url_layout.addWidget(self.url_load_button)


        self.verticalLayout_2.addLayout(self.url_layout)


        self.verticalLayout.addWidget(self.url_groupbox)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Load .cube files online...", None))
        self.database_groupbox.setTitle(QCoreApplication.translate("main_window", u"Database", None))
#if QT_CONFIG(tooltip)
        self.tree.setToolTip(QCoreApplication.translate("main_window", u"A tree consisting of molecules and their orbitals listed in the database file.\n"
"Choose one or more orbitals by selecting the wanted orbitals and click 'Load'.\n"
"\n"
"To load multiple orbitals keep the Ctrl (or Shift) key pressed during the selection process.\n"
"\n"
"To load an entire molecule, simply select the molecule row.", None))
#endif // QT_CONFIG(tooltip)
        self.combobox.setItemText(0, QCoreApplication.translate("main_window", u"No Filter", None))
        self.combobox.setItemText(1, QCoreApplication.translate("main_window", u"B3LYP", None))
        self.combobox.setItemText(2, QCoreApplication.translate("main_window", u"HSE", None))
        self.combobox.setItemText(3, QCoreApplication.translate("main_window", u"OT-RSH", None))
        self.combobox.setItemText(4, QCoreApplication.translate("main_window", u"PBE", None))

#if QT_CONFIG(tooltip)
        self.combobox.setToolTip(QCoreApplication.translate("main_window", u"Choose a filter for XC-functionals.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.line_edit.setToolTip(QCoreApplication.translate("main_window", u"Search a molecule by name.", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit.setPlaceholderText(QCoreApplication.translate("main_window", u"Enter search here...", None))
#if QT_CONFIG(tooltip)
        self.find_button.setToolTip(QCoreApplication.translate("main_window", u"Searches for the molecule entered in the line edit.", None))
#endif // QT_CONFIG(tooltip)
        self.find_button.setText(QCoreApplication.translate("main_window", u"Find", None))
#if QT_CONFIG(tooltip)
        self.database_load_button.setToolTip(QCoreApplication.translate("main_window", u"Load all selected molecules and orbitals.", None))
#endif // QT_CONFIG(tooltip)
        self.database_load_button.setText(QCoreApplication.translate("main_window", u"Load", None))
        self.url_groupbox.setTitle(QCoreApplication.translate("main_window", u"Load by URL", None))
        self.text_edit.setPlaceholderText(QCoreApplication.translate("main_window", u"Please enter URLs to be loaded directly here. To load multiple orbitals, enter each URL on a new line.", None))
        self.url_load_button.setText(QCoreApplication.translate("main_window", u"Load", None))
    # retranslateUi

