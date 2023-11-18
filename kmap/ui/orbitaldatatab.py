# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'orbitaldatatab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from kmap.controller.cubeoptions import CubeOptions
from kmap.controller.miniplots import (Mini3DKSpacePlot, MiniRealSpacePlot)
from kmap.controller.orbitaltable import OrbitalTable
from kmap.controller.polarization import Polarization
from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.controller.realplotoptions import RealPlotOptions

class Ui_orbitaldatatab(object):
    def setupUi(self, orbitaldatatab):
        if not orbitaldatatab.objectName():
            orbitaldatatab.setObjectName(u"orbitaldatatab")
        orbitaldatatab.resize(958, 537)
        self.horizontalLayout = QHBoxLayout(orbitaldatatab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scroll_area = QScrollArea(orbitaldatatab)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setMinimumSize(QSize(750, 0))
        self.scroll_area.setBaseSize(QSize(650, 0))
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.layout = QWidget()
        self.layout.setObjectName(u"layout")
        self.layout.setGeometry(QRect(0, 0, 731, 513))
        self.verticalLayout = QVBoxLayout(self.layout)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 20, 0)
        self.table = OrbitalTable(self.layout)
        self.table.setObjectName(u"table")
        self.table.setMinimumSize(QSize(0, 200))

        self.verticalLayout.addWidget(self.table)

        self.layout_2 = QHBoxLayout()
        self.layout_2.setObjectName(u"layout_2")
        self.real_space_options = RealPlotOptions(self.layout)
        self.real_space_options.setObjectName(u"real_space_options")

        self.layout_2.addWidget(self.real_space_options)

        self.mini_real_plot = MiniRealSpacePlot(self.layout)
        self.mini_real_plot.setObjectName(u"mini_real_plot")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mini_real_plot.sizePolicy().hasHeightForWidth())
        self.mini_real_plot.setSizePolicy(sizePolicy1)
        self.mini_real_plot.setFocusPolicy(Qt.WheelFocus)

        self.layout_2.addWidget(self.mini_real_plot)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_2.addItem(self.horizontalSpacer)

        self.mini_3Dkspace_plot = Mini3DKSpacePlot(self.layout)
        self.mini_3Dkspace_plot.setObjectName(u"mini_3Dkspace_plot")
        self.mini_3Dkspace_plot.setFocusPolicy(Qt.WheelFocus)

        self.layout_2.addWidget(self.mini_3Dkspace_plot)


        self.verticalLayout.addLayout(self.layout_2)

        self.polarization_layout = QHBoxLayout()
        self.polarization_layout.setObjectName(u"polarization_layout")
        self.polarization = Polarization(self.layout)
        self.polarization.setObjectName(u"polarization")

        self.polarization_layout.addWidget(self.polarization)

        self.cube_options = CubeOptions(self.layout)
        self.cube_options.setObjectName(u"cube_options")

        self.polarization_layout.addWidget(self.cube_options)


        self.verticalLayout.addLayout(self.polarization_layout)

        self.scroll_area.setWidget(self.layout)

        self.horizontalLayout.addWidget(self.scroll_area)

        self.plot_item = PyQtGraphPlot(orbitaldatatab)
        self.plot_item.setObjectName(u"plot_item")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plot_item.sizePolicy().hasHeightForWidth())
        self.plot_item.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.plot_item)


        self.retranslateUi(orbitaldatatab)

        QMetaObject.connectSlotsByName(orbitaldatatab)
    # setupUi

    def retranslateUi(self, orbitaldatatab):
        orbitaldatatab.setWindowTitle(QCoreApplication.translate("orbitaldatatab", u"Form", None))
    # retranslateUi

