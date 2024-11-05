# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sliceddatabaseoptions2.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_window(object):
    def setupUi(self, window):
        if not window.objectName():
            window.setObjectName("window")
        window.resize(442, 701)
        self.verticalLayout = QVBoxLayout(window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_groupbox = QGroupBox(window)
        self.name_groupbox.setObjectName("name_groupbox")
        font = QFont()
        font.setBold(True)
        self.name_groupbox.setFont(font)
        self.name_groupbox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_3 = QHBoxLayout(self.name_groupbox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line_edit = QLineEdit(self.name_groupbox)
        self.line_edit.setObjectName("line_edit")
        font1 = QFont()
        font1.setBold(False)
        self.line_edit.setFont(font1)
        self.line_edit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.line_edit)

        self.verticalLayout.addWidget(self.name_groupbox)

        self.other_groupbox = QGroupBox(window)
        self.other_groupbox.setObjectName("other_groupbox")
        self.other_groupbox.setFont(font)
        self.other_groupbox.setAlignment(Qt.AlignCenter)
        self.formLayout_2 = QFormLayout(self.other_groupbox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.photon_min_label = QLabel(self.other_groupbox)
        self.photon_min_label.setObjectName("photon_min_label")
        self.photon_min_label.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.photon_min_label)

        self.photon_min_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.photon_min_spinbox.setObjectName("photon_min_spinbox")
        self.photon_min_spinbox.setFont(font1)
        self.photon_min_spinbox.setAlignment(Qt.AlignCenter)
        self.photon_min_spinbox.setCorrectionMode(
            QAbstractSpinBox.CorrectToNearestValue
        )
        self.photon_min_spinbox.setKeyboardTracking(False)
        self.photon_min_spinbox.setDecimals(1)
        self.photon_min_spinbox.setValue(20.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.photon_min_spinbox)

        self.fermi_label = QLabel(self.other_groupbox)
        self.fermi_label.setObjectName("fermi_label")
        self.fermi_label.setFont(font1)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.fermi_label)

        self.fermi_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.fermi_spinbox.setObjectName("fermi_spinbox")
        self.fermi_spinbox.setFont(font1)
        self.fermi_spinbox.setAlignment(Qt.AlignCenter)
        self.fermi_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.fermi_spinbox.setKeyboardTracking(False)
        self.fermi_spinbox.setDecimals(1)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.fermi_spinbox)

        self.dk_label = QLabel(self.other_groupbox)
        self.dk_label.setObjectName("dk_label")
        self.dk_label.setFont(font1)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.dk_label)

        self.dk_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.dk_spinbox.setObjectName("dk_spinbox")
        self.dk_spinbox.setFont(font1)
        self.dk_spinbox.setAlignment(Qt.AlignCenter)
        self.dk_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.dk_spinbox.setKeyboardTracking(False)
        self.dk_spinbox.setMinimum(0.010000000000000)
        self.dk_spinbox.setMaximum(1.000000000000000)
        self.dk_spinbox.setSingleStep(0.010000000000000)
        self.dk_spinbox.setValue(0.020000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.dk_spinbox)

        self.photon_max_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.photon_max_spinbox.setObjectName("photon_max_spinbox")
        self.photon_max_spinbox.setFont(font1)
        self.photon_max_spinbox.setAlignment(Qt.AlignCenter)
        self.photon_max_spinbox.setKeyboardTracking(False)
        self.photon_max_spinbox.setDecimals(1)
        self.photon_max_spinbox.setMaximum(150.000000000000000)
        self.photon_max_spinbox.setSingleStep(1.000000000000000)
        self.photon_max_spinbox.setValue(80.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.photon_max_spinbox)

        self.photon_max_label = QLabel(self.other_groupbox)
        self.photon_max_label.setObjectName("photon_max_label")
        self.photon_max_label.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.photon_max_label)

        self.photon_step_spinbox = QDoubleSpinBox(self.other_groupbox)
        self.photon_step_spinbox.setObjectName("photon_step_spinbox")
        self.photon_step_spinbox.setFont(font1)
        self.photon_step_spinbox.setAlignment(Qt.AlignCenter)
        self.photon_step_spinbox.setDecimals(1)
        self.photon_step_spinbox.setMinimum(0.100000000000000)
        self.photon_step_spinbox.setMaximum(5.000000000000000)
        self.photon_step_spinbox.setSingleStep(0.200000000000000)
        self.photon_step_spinbox.setValue(2.000000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.photon_step_spinbox)

        self.photon_step_label = QLabel(self.other_groupbox)
        self.photon_step_label.setObjectName("photon_step_label")
        self.photon_step_label.setFont(font1)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.photon_step_label)

        self.verticalLayout.addWidget(self.other_groupbox)

        self.orientation_groupbox = QGroupBox(window)
        self.orientation_groupbox.setObjectName("orientation_groupbox")
        self.orientation_groupbox.setFont(font)
        self.orientation_groupbox.setAlignment(Qt.AlignCenter)
        self.formLayout_3 = QFormLayout(self.orientation_groupbox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.phi_label = QLabel(self.orientation_groupbox)
        self.phi_label.setObjectName("phi_label")
        self.phi_label.setFont(font1)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.phi_label)

        self.phi_spinbox = QDoubleSpinBox(self.orientation_groupbox)
        self.phi_spinbox.setObjectName("phi_spinbox")
        self.phi_spinbox.setFont(font1)
        self.phi_spinbox.setAlignment(Qt.AlignCenter)
        self.phi_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.phi_spinbox.setKeyboardTracking(False)
        self.phi_spinbox.setDecimals(1)
        self.phi_spinbox.setMinimum(-90.000000000000000)
        self.phi_spinbox.setMaximum(90.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.phi_spinbox)

        self.theta_label = QLabel(self.orientation_groupbox)
        self.theta_label.setObjectName("theta_label")
        self.theta_label.setFont(font1)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.theta_label)

        self.theta_spinbox = QDoubleSpinBox(self.orientation_groupbox)
        self.theta_spinbox.setObjectName("theta_spinbox")
        self.theta_spinbox.setFont(font1)
        self.theta_spinbox.setAlignment(Qt.AlignCenter)
        self.theta_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.theta_spinbox.setKeyboardTracking(False)
        self.theta_spinbox.setDecimals(1)
        self.theta_spinbox.setMinimum(-90.000000000000000)
        self.theta_spinbox.setMaximum(90.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.theta_spinbox)

        self.psi_label = QLabel(self.orientation_groupbox)
        self.psi_label.setObjectName("psi_label")
        self.psi_label.setFont(font1)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.psi_label)

        self.psi_spinbox = QDoubleSpinBox(self.orientation_groupbox)
        self.psi_spinbox.setObjectName("psi_spinbox")
        self.psi_spinbox.setFont(font1)
        self.psi_spinbox.setAlignment(Qt.AlignCenter)
        self.psi_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.psi_spinbox.setKeyboardTracking(False)
        self.psi_spinbox.setDecimals(1)
        self.psi_spinbox.setMinimum(-90.000000000000000)
        self.psi_spinbox.setMaximum(90.000000000000000)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.psi_spinbox)

        self.verticalLayout.addWidget(self.orientation_groupbox)

        self.polarization_groupbox = QGroupBox(window)
        self.polarization_groupbox.setObjectName("polarization_groupbox")
        self.polarization_groupbox.setFont(font)
        self.polarization_groupbox.setAlignment(Qt.AlignCenter)
        self.formLayout = QFormLayout(self.polarization_groupbox)
        self.formLayout.setObjectName("formLayout")
        self.polarization_label = QLabel(self.polarization_groupbox)
        self.polarization_label.setObjectName("polarization_label")
        self.polarization_label.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.polarization_label)

        self.polarization_combobox = QComboBox(self.polarization_groupbox)
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.addItem("")
        self.polarization_combobox.setObjectName("polarization_combobox")
        self.polarization_combobox.setFont(font1)
        self.polarization_combobox.setMaxVisibleItems(8)
        self.polarization_combobox.setMaxCount(8)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.polarization_combobox)

        self.angle_label = QLabel(self.polarization_groupbox)
        self.angle_label.setObjectName("angle_label")
        self.angle_label.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.angle_label)

        self.angle_spinbox = QDoubleSpinBox(self.polarization_groupbox)
        self.angle_spinbox.setObjectName("angle_spinbox")
        self.angle_spinbox.setFont(font1)
        self.angle_spinbox.setAlignment(Qt.AlignCenter)
        self.angle_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.angle_spinbox.setKeyboardTracking(False)
        self.angle_spinbox.setDecimals(1)
        self.angle_spinbox.setMaximum(90.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.angle_spinbox)

        self.azimuth_label = QLabel(self.polarization_groupbox)
        self.azimuth_label.setObjectName("azimuth_label")
        self.azimuth_label.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.azimuth_label)

        self.azimuth_spinbox = QDoubleSpinBox(self.polarization_groupbox)
        self.azimuth_spinbox.setObjectName("azimuth_spinbox")
        self.azimuth_spinbox.setFont(font1)
        self.azimuth_spinbox.setAlignment(Qt.AlignCenter)
        self.azimuth_spinbox.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.azimuth_spinbox.setKeyboardTracking(False)
        self.azimuth_spinbox.setDecimals(1)
        self.azimuth_spinbox.setMaximum(360.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.azimuth_spinbox)

        self.symmetrization_label = QLabel(self.polarization_groupbox)
        self.symmetrization_label.setObjectName("symmetrization_label")
        self.symmetrization_label.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.symmetrization_label)

        self.symmetrization_combobox = QComboBox(self.polarization_groupbox)
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.addItem("")
        self.symmetrization_combobox.setObjectName("symmetrization_combobox")
        self.symmetrization_combobox.setFont(font1)
        self.symmetrization_combobox.setMaxVisibleItems(7)
        self.symmetrization_combobox.setMaxCount(7)

        self.formLayout.setWidget(
            3, QFormLayout.FieldRole, self.symmetrization_combobox
        )

        self.verticalLayout.addWidget(self.polarization_groupbox)

        self.retranslateUi(window)

        self.polarization_combobox.setCurrentIndex(0)
        self.symmetrization_combobox.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(window)

    # setupUi

    def retranslateUi(self, window):
        window.setWindowTitle(QCoreApplication.translate("window", "Options", None))
        self.name_groupbox.setTitle(QCoreApplication.translate("window", "Name", None))
        self.line_edit.setPlaceholderText(
            QCoreApplication.translate("window", "Enter name here...", None)
        )
        self.other_groupbox.setTitle(
            QCoreApplication.translate("window", "Options", None)
        )
        self.photon_min_label.setText(
            QCoreApplication.translate("window", "Minimal Photon Energy:", None)
        )
        self.photon_min_spinbox.setSuffix(
            QCoreApplication.translate("window", "  eV", None)
        )
        self.fermi_label.setText(
            QCoreApplication.translate("window", "Fermi Energy:", None)
        )
        self.fermi_spinbox.setSuffix(QCoreApplication.translate("window", "  eV", None))
        self.dk_label.setText(
            QCoreApplication.translate("window", "Resolution dk:", None)
        )
        self.dk_spinbox.setSuffix(
            QCoreApplication.translate("window", "  \u212b^-1", None)
        )
        self.photon_max_spinbox.setSuffix(
            QCoreApplication.translate("window", " eV", None)
        )
        self.photon_max_label.setText(
            QCoreApplication.translate("window", "Maximal Photon Energy:", None)
        )
        self.photon_step_spinbox.setSuffix(
            QCoreApplication.translate("window", " eV", None)
        )
        self.photon_step_label.setText(
            QCoreApplication.translate("window", "Stepsize Photon Energy:", None)
        )
        self.orientation_groupbox.setTitle(
            QCoreApplication.translate("window", "Orientation", None)
        )
        self.phi_label.setText(QCoreApplication.translate("window", "Phi:  ", None))
        self.phi_spinbox.setSuffix(QCoreApplication.translate("window", "\u00b0", None))
        self.theta_label.setText(QCoreApplication.translate("window", "Theta:  ", None))
        self.theta_spinbox.setSuffix(
            QCoreApplication.translate("window", "\u00b0", None)
        )
        self.psi_label.setText(QCoreApplication.translate("window", "Psi:  ", None))
        self.psi_spinbox.setSuffix(QCoreApplication.translate("window", "\u00b0", None))
        self.polarization_groupbox.setTitle(
            QCoreApplication.translate("window", "Polarization", None)
        )
        self.polarization_label.setText(
            QCoreApplication.translate("window", "Polarization:", None)
        )
        self.polarization_combobox.setItemText(
            0, QCoreApplication.translate("window", "No |A.k|^2", None)
        )
        self.polarization_combobox.setItemText(
            1, QCoreApplication.translate("window", "Toroid (p-pol)", None)
        )
        self.polarization_combobox.setItemText(
            2, QCoreApplication.translate("window", "p-polarized", None)
        )
        self.polarization_combobox.setItemText(
            3, QCoreApplication.translate("window", "s-polarized", None)
        )
        self.polarization_combobox.setItemText(
            4, QCoreApplication.translate("window", "unpolarized", None)
        )
        self.polarization_combobox.setItemText(
            5, QCoreApplication.translate("window", "circular+", None)
        )
        self.polarization_combobox.setItemText(
            6, QCoreApplication.translate("window", "circular-", None)
        )
        self.polarization_combobox.setItemText(
            7, QCoreApplication.translate("window", "CDAD", None)
        )

        self.angle_label.setText(QCoreApplication.translate("window", "Angle:", None))
        self.angle_spinbox.setSuffix(
            QCoreApplication.translate("window", "\u00b0", None)
        )
        self.azimuth_label.setText(
            QCoreApplication.translate("window", "Azimuth:", None)
        )
        self.azimuth_spinbox.setSuffix(
            QCoreApplication.translate("window", "\u00b0", None)
        )
        self.symmetrization_label.setText(
            QCoreApplication.translate("window", "Symmetrization:", None)
        )
        self.symmetrization_combobox.setItemText(
            0, QCoreApplication.translate("window", "No Symmetry", None)
        )
        self.symmetrization_combobox.setItemText(
            1, QCoreApplication.translate("window", "2-Fold", None)
        )
        self.symmetrization_combobox.setItemText(
            2, QCoreApplication.translate("window", "2-Fold + Mirror", None)
        )
        self.symmetrization_combobox.setItemText(
            3, QCoreApplication.translate("window", "3-Fold", None)
        )
        self.symmetrization_combobox.setItemText(
            4, QCoreApplication.translate("window", "3-Fold + Mirror", None)
        )
        self.symmetrization_combobox.setItemText(
            5, QCoreApplication.translate("window", "4-Fold", None)
        )
        self.symmetrization_combobox.setItemText(
            6, QCoreApplication.translate("window", "4-Fold + Mirror", None)
        )

    # retranslateUi
