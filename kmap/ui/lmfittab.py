# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lmfittab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from kmap.controller.pyqtgraphplot import PyQtGraphPlot

class Ui_lmfittab(object):
    def setupUi(self, lmfittab):
        if not lmfittab.objectName():
            lmfittab.setObjectName(u"lmfittab")
        lmfittab.resize(1205, 782)
        lmfittab.setMinimumSize(QSize(0, 0))
        lmfittab.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(lmfittab)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.scroll_area = QScrollArea(lmfittab)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setMinimumSize(QSize(650, 0))
        self.scroll_area.setMaximumSize(QSize(650, 16777215))
        self.scroll_area.setBaseSize(QSize(0, 0))
        self.scroll_area.setWidgetResizable(True)
        self.layout_7 = QWidget()
        self.layout_7.setObjectName(u"layout_7")
        self.layout_7.setGeometry(QRect(0, 0, 648, 381))
        self.scroll_area.setWidget(self.layout_7)

        self.layout.addWidget(self.scroll_area)


        self.verticalLayout.addLayout(self.layout)

        self.layout_2 = QHBoxLayout()
        self.layout_2.setSpacing(5)
        self.layout_2.setObjectName(u"layout_2")
        self.layout_6 = QVBoxLayout()
        self.layout_6.setObjectName(u"layout_6")
        self.sliced_label = QLabel(lmfittab)
        self.sliced_label.setObjectName(u"sliced_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sliced_label.sizePolicy().hasHeightForWidth())
        self.sliced_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setBold(True)
        self.sliced_label.setFont(font)
        self.sliced_label.setAlignment(Qt.AlignCenter)

        self.layout_6.addWidget(self.sliced_label)

        self.sliced_plot = PyQtGraphPlot(lmfittab)
        self.sliced_plot.setObjectName(u"sliced_plot")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sliced_plot.sizePolicy().hasHeightForWidth())
        self.sliced_plot.setSizePolicy(sizePolicy2)
        self.sliced_plot.setMinimumSize(QSize(0, 200))
        self.sliced_plot.setMaximumSize(QSize(16777215, 350))

        self.layout_6.addWidget(self.sliced_plot)


        self.layout_2.addLayout(self.layout_6)

        self.layout_5 = QVBoxLayout()
        self.layout_5.setObjectName(u"layout_5")
        self.selected_label = QLabel(lmfittab)
        self.selected_label.setObjectName(u"selected_label")
        sizePolicy1.setHeightForWidth(self.selected_label.sizePolicy().hasHeightForWidth())
        self.selected_label.setSizePolicy(sizePolicy1)
        self.selected_label.setFont(font)
        self.selected_label.setAlignment(Qt.AlignCenter)

        self.layout_5.addWidget(self.selected_label)

        self.selected_plot = PyQtGraphPlot(lmfittab)
        self.selected_plot.setObjectName(u"selected_plot")
        sizePolicy2.setHeightForWidth(self.selected_plot.sizePolicy().hasHeightForWidth())
        self.selected_plot.setSizePolicy(sizePolicy2)
        self.selected_plot.setMinimumSize(QSize(0, 200))
        self.selected_plot.setMaximumSize(QSize(16777215, 350))

        self.layout_5.addWidget(self.selected_plot)


        self.layout_2.addLayout(self.layout_5)

        self.layout_4 = QVBoxLayout()
        self.layout_4.setObjectName(u"layout_4")
        self.sum_label = QLabel(lmfittab)
        self.sum_label.setObjectName(u"sum_label")
        sizePolicy1.setHeightForWidth(self.sum_label.sizePolicy().hasHeightForWidth())
        self.sum_label.setSizePolicy(sizePolicy1)
        self.sum_label.setFont(font)
        self.sum_label.setAlignment(Qt.AlignCenter)

        self.layout_4.addWidget(self.sum_label)

        self.sum_plot = PyQtGraphPlot(lmfittab)
        self.sum_plot.setObjectName(u"sum_plot")
        sizePolicy2.setHeightForWidth(self.sum_plot.sizePolicy().hasHeightForWidth())
        self.sum_plot.setSizePolicy(sizePolicy2)
        self.sum_plot.setMinimumSize(QSize(0, 200))
        self.sum_plot.setMaximumSize(QSize(16777215, 350))

        self.layout_4.addWidget(self.sum_plot)


        self.layout_2.addLayout(self.layout_4)

        self.layout_3 = QVBoxLayout()
        self.layout_3.setObjectName(u"layout_3")
        self.residual_label = QLabel(lmfittab)
        self.residual_label.setObjectName(u"residual_label")
        sizePolicy1.setHeightForWidth(self.residual_label.sizePolicy().hasHeightForWidth())
        self.residual_label.setSizePolicy(sizePolicy1)
        self.residual_label.setFont(font)
        self.residual_label.setAlignment(Qt.AlignCenter)

        self.layout_3.addWidget(self.residual_label)

        self.residual_plot = PyQtGraphPlot(lmfittab)
        self.residual_plot.setObjectName(u"residual_plot")
        sizePolicy2.setHeightForWidth(self.residual_plot.sizePolicy().hasHeightForWidth())
        self.residual_plot.setSizePolicy(sizePolicy2)
        self.residual_plot.setMinimumSize(QSize(0, 200))
        self.residual_plot.setMaximumSize(QSize(16777215, 350))

        self.layout_3.addWidget(self.residual_plot)


        self.layout_2.addLayout(self.layout_3)


        self.verticalLayout.addLayout(self.layout_2)


        self.retranslateUi(lmfittab)

        QMetaObject.connectSlotsByName(lmfittab)
    # setupUi

    def retranslateUi(self, lmfittab):
        lmfittab.setWindowTitle(QCoreApplication.translate("lmfittab", u"Form", None))
#if QT_CONFIG(tooltip)
        self.sliced_label.setToolTip(QCoreApplication.translate("lmfittab", u"Displays the current slice from the sliced data loaded.\n"
"\n"
"The slice has been interpolated and, if checked, also smoothed.", None))
#endif // QT_CONFIG(tooltip)
        self.sliced_label.setText(QCoreApplication.translate("lmfittab", u"Sliced Data", None))
#if QT_CONFIG(tooltip)
        self.selected_label.setToolTip(QCoreApplication.translate("lmfittab", u"Displays the currently selected orbital.\n"
"\n"
"The calculation has been performed with the \"initial\" values.\n"
"\n"
"The kmap displayed has been interpolated and, if checked, smoothed. ", None))
#endif // QT_CONFIG(tooltip)
        self.selected_label.setText(QCoreApplication.translate("lmfittab", u"Selected Orbital", None))
        self.sum_label.setText(QCoreApplication.translate("lmfittab", u"\u03a3 Weight * Orbital + Background", None))
#if QT_CONFIG(tooltip)
        self.residual_label.setToolTip(QCoreApplication.translate("lmfittab", u"<html><head/><body><p>Sliced Data - \u03a3 Weight * Orbital - Background</p><p><br/></p><p>Displays the current reduced Chi^2 value of the data displayed</p><p>in the residual plot (region restriction, interpolation etc. already included).</p><p><br/></p><p>Reduced Chi^2 = Data^2 / (N-n)</p><p>N ... Number of non-nan and non-zero data points.</p><p>n ... Degrees of freedom (number of parameters set to vary).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.residual_label.setText(QCoreApplication.translate("lmfittab", u"Residual", None))
    # retranslateUi

