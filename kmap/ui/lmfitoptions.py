# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitoptions.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_lmfit(object):
    def setupUi(self, lmfit):
        if not lmfit.objectName():
            lmfit.setObjectName(u"lmfit")
        lmfit.resize(656, 180)
        self.horizontalLayout = QHBoxLayout(lmfit)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout = QGroupBox(lmfit)
        self.layout.setObjectName(u"layout")
        font = QFont()
        font.setBold(True)
        self.layout.setFont(font)
        self.layout.setAlignment(Qt.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.layout)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.layout_2 = QGridLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.method_combobox = QComboBox(self.layout)
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.addItem("")
        self.method_combobox.setObjectName(u"method_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.method_combobox.sizePolicy().hasHeightForWidth())
        self.method_combobox.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(False)
        self.method_combobox.setFont(font1)

        self.layout_2.addWidget(self.method_combobox, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slice_combobox = QComboBox(self.layout)
        self.slice_combobox.addItem("")
        self.slice_combobox.addItem("")
        self.slice_combobox.addItem("")
        self.slice_combobox.addItem("")
        self.slice_combobox.setObjectName(u"slice_combobox")
        self.slice_combobox.setFont(font1)

        self.horizontalLayout_2.addWidget(self.slice_combobox)

        self.from_slice_spinbox = QSpinBox(self.layout)
        self.from_slice_spinbox.setObjectName(u"from_slice_spinbox")
        self.from_slice_spinbox.setEnabled(False)
        self.from_slice_spinbox.setFont(font1)
        self.from_slice_spinbox.setFrame(False)
        self.from_slice_spinbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.from_slice_spinbox.setKeyboardTracking(False)
        self.from_slice_spinbox.setMaximum(1000000)

        self.horizontalLayout_2.addWidget(self.from_slice_spinbox)

        self.to_slice_spinbox = QSpinBox(self.layout)
        self.to_slice_spinbox.setObjectName(u"to_slice_spinbox")
        self.to_slice_spinbox.setEnabled(False)
        self.to_slice_spinbox.setFont(font1)
        self.to_slice_spinbox.setKeyboardTracking(False)
        self.to_slice_spinbox.setMaximum(10000000)
        self.to_slice_spinbox.setValue(1)

        self.horizontalLayout_2.addWidget(self.to_slice_spinbox)


        self.layout_2.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)

        self.background_label = QLabel(self.layout)
        self.background_label.setObjectName(u"background_label")
        self.background_label.setFont(font1)

        self.layout_2.addWidget(self.background_label, 3, 0, 1, 1)

        self.region_label = QLabel(self.layout)
        self.region_label.setObjectName(u"region_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.region_label.sizePolicy().hasHeightForWidth())
        self.region_label.setSizePolicy(sizePolicy1)
        self.region_label.setMinimumSize(QSize(120, 0))
        self.region_label.setFont(font1)

        self.layout_2.addWidget(self.region_label, 1, 0, 1, 1)

        self.fit_button = QPushButton(self.layout)
        self.fit_button.setObjectName(u"fit_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fit_button.sizePolicy().hasHeightForWidth())
        self.fit_button.setSizePolicy(sizePolicy2)
        self.fit_button.setMinimumSize(QSize(150, 0))
        self.fit_button.setFont(font1)

        self.layout_2.addWidget(self.fit_button, 0, 0, 1, 1)

        self.background_combobox = QComboBox(self.layout)
        self.background_combobox.setObjectName(u"background_combobox")
        self.background_combobox.setMaximumSize(QSize(450, 16777215))
        self.background_combobox.setFont(font1)
        self.background_combobox.setEditable(True)

        self.layout_2.addWidget(self.background_combobox, 3, 1, 1, 1)

        self.region_comboBox = QComboBox(self.layout)
        self.region_comboBox.addItem("")
        self.region_comboBox.addItem("")
        self.region_comboBox.addItem("")
        self.region_comboBox.addItem("")
        self.region_comboBox.addItem("")
        self.region_comboBox.setObjectName(u"region_comboBox")
        self.region_comboBox.setFont(font1)

        self.layout_2.addWidget(self.region_comboBox, 1, 1, 1, 1)

        self.method_label = QLabel(self.layout)
        self.method_label.setObjectName(u"method_label")
        sizePolicy1.setHeightForWidth(self.method_label.sizePolicy().hasHeightForWidth())
        self.method_label.setSizePolicy(sizePolicy1)
        self.method_label.setMinimumSize(QSize(120, 0))
        self.method_label.setFont(font1)

        self.layout_2.addWidget(self.method_label, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.layout_2)


        self.horizontalLayout.addWidget(self.layout)


        self.retranslateUi(lmfit)

        QMetaObject.connectSlotsByName(lmfit)
    # setupUi

    def retranslateUi(self, lmfit):
        lmfit.setWindowTitle(QCoreApplication.translate("lmfit", u"Form", None))
        self.layout.setTitle(QCoreApplication.translate("lmfit", u"LM-Fit", None))
        self.method_combobox.setItemText(0, QCoreApplication.translate("lmfit", u"Levenberg-Marquardt (leastsq)", None))
        self.method_combobox.setItemText(1, QCoreApplication.translate("lmfit", u"Matrix Inversion (matrix_inversion)", None))
        self.method_combobox.setItemText(2, QCoreApplication.translate("lmfit", u"Least-Square (least_squares)", None))
        self.method_combobox.setItemText(3, QCoreApplication.translate("lmfit", u"Differential Evolution (differential_evolution)", None))
        self.method_combobox.setItemText(4, QCoreApplication.translate("lmfit", u"Brute Force (brute)", None))
        self.method_combobox.setItemText(5, QCoreApplication.translate("lmfit", u"Basinhopping (basinhopping)", None))
        self.method_combobox.setItemText(6, QCoreApplication.translate("lmfit", u"Adaptive Memory Programming for Global Optimization (ampgo)", None))
        self.method_combobox.setItemText(7, QCoreApplication.translate("lmfit", u"Nelder-Method (nelder)", None))
        self.method_combobox.setItemText(8, QCoreApplication.translate("lmfit", u"L-BFGS-B (lbfgsb)", None))
        self.method_combobox.setItemText(9, QCoreApplication.translate("lmfit", u"Powell (powell)", None))
        self.method_combobox.setItemText(10, QCoreApplication.translate("lmfit", u"Conjugate-Gradient (cg)", None))
        self.method_combobox.setItemText(11, QCoreApplication.translate("lmfit", u"Cobyla (cobyla)", None))
        self.method_combobox.setItemText(12, QCoreApplication.translate("lmfit", u"BFGS (bfgs)", None))
        self.method_combobox.setItemText(13, QCoreApplication.translate("lmfit", u"Truncated Newton (tnc)", None))
        self.method_combobox.setItemText(14, QCoreApplication.translate("lmfit", u"Dual Annealing optimization (dual_annealing)", None))

        self.slice_combobox.setItemText(0, QCoreApplication.translate("lmfit", u"Only this Slice", None))
        self.slice_combobox.setItemText(1, QCoreApplication.translate("lmfit", u"All Slices Individually", None))
        self.slice_combobox.setItemText(2, QCoreApplication.translate("lmfit", u"All Slices Combined", None))
        self.slice_combobox.setItemText(3, QCoreApplication.translate("lmfit", u"Some Slices", None))

        self.from_slice_spinbox.setPrefix(QCoreApplication.translate("lmfit", u"From: ", None))
        self.to_slice_spinbox.setPrefix(QCoreApplication.translate("lmfit", u"To: ", None))
        self.background_label.setText(QCoreApplication.translate("lmfit", u"Background Eq.:", None))
        self.region_label.setText(QCoreApplication.translate("lmfit", u"Fit Region:", None))
        self.fit_button.setText(QCoreApplication.translate("lmfit", u"Fit", None))
#if QT_CONFIG(tooltip)
        self.background_combobox.setToolTip(QCoreApplication.translate("lmfit", u"Enter an equation for a region-dependency you want to\n"
"impose onto the background. Press return key to accept.\n"
"\n"
"The equation entered will be parsed with eval() and can\n"
"contain any number of variables as well as all numpy,\n"
"math or builtin methods. Prefix the first with 'np.' and\n"
"the second with 'math.'.\n"
"\n"
"The variables will be added to be tree and can be subject\n"
"to fitting like any other variable. You can use lower and\n"
"upper case letters, underscores and numbers (can't start\n"
"with numbers).\n"
"\n"
"Example: 2D Gaussian Curve centered at (x_m, y_m) and\n"
"with a standard deviation of (std_x, std_y):\n"
"\n"
"a*np.exp(-((x+x_m)**2/(2*std_x**2)+(y-y_m)**2)/(2*std_y**2))+c\n"
" ", None))
#endif // QT_CONFIG(tooltip)
        self.background_combobox.setCurrentText(QCoreApplication.translate("lmfit", u"Enter background equation here...", None))
        self.region_comboBox.setItemText(0, QCoreApplication.translate("lmfit", u"Entire kMap", None))
        self.region_comboBox.setItemText(1, QCoreApplication.translate("lmfit", u"Only ROI", None))
        self.region_comboBox.setItemText(2, QCoreApplication.translate("lmfit", u"Only Annulus", None))
        self.region_comboBox.setItemText(3, QCoreApplication.translate("lmfit", u"Except ROI", None))
        self.region_comboBox.setItemText(4, QCoreApplication.translate("lmfit", u"Except Annulus", None))

        self.method_label.setText(QCoreApplication.translate("lmfit", u"Method:", None))
    # retranslateUi

