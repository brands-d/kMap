# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'slicedcubefileoptions.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_window(object):
    def setupUi(self, window):
        if not window.objectName():
            window.setObjectName(u"window")
        window.resize(442, 273)
        self.verticalLayout = QVBoxLayout(window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.name_groupbox = QGroupBox(window)
        self.name_groupbox.setObjectName(u"name_groupbox")
        font = QFont()
        font.setBold(True)
        self.name_groupbox.setFont(font)
        self.name_groupbox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_3 = QHBoxLayout(self.name_groupbox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.line_edit = QLineEdit(self.name_groupbox)
        self.line_edit.setObjectName(u"line_edit")
        font1 = QFont()
        font1.setBold(False)
        self.line_edit.setFont(font1)
        self.line_edit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.line_edit)


        self.verticalLayout.addWidget(self.name_groupbox)

        self.other_groupbox = QGroupBox(window)
        self.other_groupbox.setObjectName(u"other_groupbox")
        self.other_groupbox.setFont(font)
        self.other_groupbox.setAlignment(Qt.AlignCenter)
        self.formLayout_2 = QFormLayout(self.other_groupbox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.Ekin_max_label = QLabel(self.other_groupbox)
        self.Ekin_max_label.setObjectName(u"Ekin_max_label")
        self.Ekin_max_label.setFont(font1)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.Ekin_max_label)

        self.Ekin_max_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.Ekin_max_spinbox.setObjectName(u"Ekin_max_spinbox")
        self.Ekin_max_spinbox.setFont(font1)
        self.Ekin_max_spinbox.setAlignment(Qt.AlignCenter)
        self.Ekin_max_spinbox.setKeyboardTracking(False)
        self.Ekin_max_spinbox.setDecimals(1)
        self.Ekin_max_spinbox.setMinimum(50.000000000000000)
        self.Ekin_max_spinbox.setMaximum(300.000000000000000)
        self.Ekin_max_spinbox.setSingleStep(1.000000000000000)
        self.Ekin_max_spinbox.setValue(150.000000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.Ekin_max_spinbox)

        self.dk3D_step_label = QLabel(self.other_groupbox)
        self.dk3D_step_label.setObjectName(u"dk3D_step_label")
        self.dk3D_step_label.setFont(font1)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.dk3D_step_label)

        self.dk3D_step_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.dk3D_step_spinbox.setObjectName(u"dk3D_step_spinbox")
        self.dk3D_step_spinbox.setFont(font1)
        self.dk3D_step_spinbox.setAlignment(Qt.AlignCenter)
        self.dk3D_step_spinbox.setDecimals(2)
        self.dk3D_step_spinbox.setMinimum(0.050000000000000)
        self.dk3D_step_spinbox.setMaximum(0.300000000000000)
        self.dk3D_step_spinbox.setSingleStep(0.010000000000000)
        self.dk3D_step_spinbox.setValue(0.150000000000000)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.dk3D_step_spinbox)

        self.domain_label = QLabel(self.other_groupbox)
        self.domain_label.setObjectName(u"domain_label")
        self.domain_label.setFont(font1)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.domain_label)

        self.domain_combobox = QComboBox(self.other_groupbox)
        self.domain_combobox.addItem("")
        self.domain_combobox.addItem("")
        self.domain_combobox.setObjectName(u"domain_combobox")
        self.domain_combobox.setFont(font1)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.domain_combobox)

        self.value_label = QLabel(self.other_groupbox)
        self.value_label.setObjectName(u"value_label")
        self.value_label.setFont(font1)

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.value_label)

        self.value_combobox = QComboBox(self.other_groupbox)
        self.value_combobox.addItem("")
        self.value_combobox.addItem("")
        self.value_combobox.addItem("")
        self.value_combobox.addItem("")
        self.value_combobox.setObjectName(u"value_combobox")
        self.value_combobox.setFont(font1)

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.value_combobox)


        self.verticalLayout.addWidget(self.other_groupbox)


        self.retranslateUi(window)

        QMetaObject.connectSlotsByName(window)
    # setupUi

    def retranslateUi(self, window):
        window.setWindowTitle(QCoreApplication.translate("window", u"Options", None))
        self.name_groupbox.setTitle(QCoreApplication.translate("window", u"Name", None))
        self.line_edit.setPlaceholderText(QCoreApplication.translate("window", u"Enter name here...", None))
        self.other_groupbox.setTitle(QCoreApplication.translate("window", u"Options", None))
        self.Ekin_max_label.setText(QCoreApplication.translate("window", u"Maximal Kinetic Energy:", None))
        self.Ekin_max_spinbox.setSuffix(QCoreApplication.translate("window", u" eV", None))
        self.dk3D_step_label.setText(QCoreApplication.translate("window", u"Step Size in k-Space:", None))
        self.dk3D_step_spinbox.setSuffix(QCoreApplication.translate("window", u"\u212b", None))
        self.domain_label.setText(QCoreApplication.translate("window", u"Choose Domain:", None))
        self.domain_combobox.setItemText(0, QCoreApplication.translate("window", u"real space", None))
        self.domain_combobox.setItemText(1, QCoreApplication.translate("window", u"momentum space", None))

        self.value_label.setText(QCoreApplication.translate("window", u"Choose Function value:", None))
        self.value_combobox.setItemText(0, QCoreApplication.translate("window", u"real part", None))
        self.value_combobox.setItemText(1, QCoreApplication.translate("window", u"imaginary part", None))
        self.value_combobox.setItemText(2, QCoreApplication.translate("window", u"absolute value", None))
        self.value_combobox.setItemText(3, QCoreApplication.translate("window", u"square of absolute value", None))

    # retranslateUi

