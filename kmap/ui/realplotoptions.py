# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'realplotoptions.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(150, 322)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.reset_camera_button = QPushButton(Form)
        self.reset_camera_button.setObjectName(u"reset_camera_button")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_camera_button.sizePolicy().hasHeightForWidth())
        self.reset_camera_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.reset_camera_button)

        self.iso_label = QLabel(Form)
        self.iso_label.setObjectName(u"iso_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.iso_label.sizePolicy().hasHeightForWidth())
        self.iso_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.iso_label)

        self.iso_spinbox = QDoubleSpinBox(Form)
        self.iso_spinbox.setObjectName(u"iso_spinbox")
        self.iso_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.iso_spinbox.setKeyboardTracking(False)
        self.iso_spinbox.setMinimum(0.010000000000000)
        self.iso_spinbox.setMaximum(2.000000000000000)
        self.iso_spinbox.setSingleStep(0.010000000000000)
        self.iso_spinbox.setValue(0.200000000000000)

        self.verticalLayout.addWidget(self.iso_spinbox)

        self.show_label = QLabel(Form)
        self.show_label.setObjectName(u"show_label")
        sizePolicy1.setHeightForWidth(self.show_label.sizePolicy().hasHeightForWidth())
        self.show_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.show_label)

        self.show_grid_checkbox = QCheckBox(Form)
        self.show_grid_checkbox.setObjectName(u"show_grid_checkbox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.show_grid_checkbox.sizePolicy().hasHeightForWidth())
        self.show_grid_checkbox.setSizePolicy(sizePolicy2)
        self.show_grid_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_grid_checkbox)

        self.show_isosurface_checkbox = QCheckBox(Form)
        self.show_isosurface_checkbox.setObjectName(u"show_isosurface_checkbox")
        sizePolicy.setHeightForWidth(self.show_isosurface_checkbox.sizePolicy().hasHeightForWidth())
        self.show_isosurface_checkbox.setSizePolicy(sizePolicy)
        self.show_isosurface_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_isosurface_checkbox)

        self.show_bond_checkbox = QCheckBox(Form)
        self.show_bond_checkbox.setObjectName(u"show_bond_checkbox")
        sizePolicy2.setHeightForWidth(self.show_bond_checkbox.sizePolicy().hasHeightForWidth())
        self.show_bond_checkbox.setSizePolicy(sizePolicy2)
        self.show_bond_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_bond_checkbox)

        self.show_photon_checkbox = QCheckBox(Form)
        self.show_photon_checkbox.setObjectName(u"show_photon_checkbox")
        self.show_photon_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_photon_checkbox)

        self.show_hemisphere_checkbox = QCheckBox(Form)
        self.show_hemisphere_checkbox.setObjectName(u"show_hemisphere_checkbox")
        self.show_hemisphere_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_hemisphere_checkbox)

        self.show_axis_checkbox = QCheckBox(Form)
        self.show_axis_checkbox.setObjectName(u"show_axis_checkbox")
        self.show_axis_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.show_axis_checkbox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.reset_camera_button.setText(QCoreApplication.translate("Form", u"Reset Camera", None))
        self.iso_label.setText(QCoreApplication.translate("Form", u"Iso-Value:", None))
        self.show_label.setText(QCoreApplication.translate("Form", u"Show:", None))
        self.show_grid_checkbox.setText(QCoreApplication.translate("Form", u"Grid", None))
        self.show_isosurface_checkbox.setText(QCoreApplication.translate("Form", u"Isosurface", None))
        self.show_bond_checkbox.setText(QCoreApplication.translate("Form", u"Bonds", None))
        self.show_photon_checkbox.setText(QCoreApplication.translate("Form", u"Photon", None))
        self.show_hemisphere_checkbox.setText(QCoreApplication.translate("Form", u"Hemisphere", None))
#if QT_CONFIG(tooltip)
        self.show_axis_checkbox.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" color:#ff0000;\">x-axis in red</span></p><p><span style=\" color:#00ff00;\">y-axis in green</span></p><p><span style=\" color:#0000ff;\">z-axis in blue</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.show_axis_checkbox.setText(QCoreApplication.translate("Form", u"Axis", None))
    # retranslateUi

