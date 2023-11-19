# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfitresult.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_lmfitresult(object):
    def setupUi(self, lmfitresult):
        if not lmfitresult.objectName():
            lmfitresult.setObjectName(u"lmfitresult")
        lmfitresult.resize(724, 114)
        self.horizontalLayout = QHBoxLayout(lmfitresult)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.group_box = QGroupBox(lmfitresult)
        self.group_box.setObjectName(u"group_box")
        font = QFont()
        font.setBold(True)
        self.group_box.setFont(font)
        self.group_box.setAlignment(Qt.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.group_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_2 = QHBoxLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.type_value = QLabel(self.group_box)
        self.type_value.setObjectName(u"type_value")
        font1 = QFont()
        font1.setBold(False)
        self.type_value.setFont(font1)

        self.layout_2.addWidget(self.type_value)

        self.type_label = QLabel(self.group_box)
        self.type_label.setObjectName(u"type_label")
        self.type_label.setFont(font1)

        self.layout_2.addWidget(self.type_label)


        self.verticalLayout.addLayout(self.layout_2)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.result_button = QPushButton(self.group_box)
        self.result_button.setObjectName(u"result_button")
        self.result_button.setEnabled(True)
        self.result_button.setFont(font1)

        self.layout.addWidget(self.result_button)

        self.plot_button = QPushButton(self.group_box)
        self.plot_button.setObjectName(u"plot_button")
        self.plot_button.setEnabled(True)
        self.plot_button.setFont(font1)

        self.layout.addWidget(self.plot_button)

        self.correlation_button = QPushButton(self.group_box)
        self.correlation_button.setObjectName(u"correlation_button")
        self.correlation_button.setEnabled(True)
        self.correlation_button.setFont(font1)

        self.layout.addWidget(self.correlation_button)


        self.verticalLayout.addLayout(self.layout)


        self.horizontalLayout.addWidget(self.group_box)


        self.retranslateUi(lmfitresult)

        QMetaObject.connectSlotsByName(lmfitresult)
    # setupUi

    def retranslateUi(self, lmfitresult):
        lmfitresult.setWindowTitle(QCoreApplication.translate("lmfitresult", u"Form", None))
        self.group_box.setTitle(QCoreApplication.translate("lmfitresult", u"LM - Fit Result", None))
        self.type_value.setText(QCoreApplication.translate("lmfitresult", u"Type:", None))
        self.type_label.setText("")
        self.result_button.setText(QCoreApplication.translate("lmfitresult", u"Print Result", None))
#if QT_CONFIG(tooltip)
        self.plot_button.setToolTip(QCoreApplication.translate("lmfitresult", u"Opens new Tab to display the results.\n"
"\n"
"Only available for \"All Slices Individually\" fits.", None))
#endif // QT_CONFIG(tooltip)
        self.plot_button.setText(QCoreApplication.translate("lmfitresult", u"Open Plot", None))
#if QT_CONFIG(tooltip)
        self.correlation_button.setToolTip(QCoreApplication.translate("lmfitresult", u"Prints the correlation coefficients of the covariance matrix to standard output.", None))
#endif // QT_CONFIG(tooltip)
        self.correlation_button.setText(QCoreApplication.translate("lmfitresult", u"Print Correlation", None))
    # retranslateUi

