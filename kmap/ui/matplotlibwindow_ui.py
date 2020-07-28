from kmap import __directory__
from kmap.ui.abstract_ui import AbstractUI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtWidgets import (
    QHBoxLayout, QGridLayout, QDoubleSpinBox, QComboBox,
    QSpinBox, QWidget, QLabel, QPushButton, QCheckBox)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT)


class MatplotlibWindowUI(AbstractUI):

    def _initialize_content(self):

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setGeometry(200, 300, 500, 500)
        self.setWindowTitle(self.name)
        self.setWindowModality(Qt.WindowModal)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        canvas = FigureCanvas(self.figure)
        canvas.setSizePolicy(QSP.Expanding, QSP.Expanding)
        self.addToolBar(NavigationToolbar2QT(canvas, self))

        main_layout = QHBoxLayout()
        main_layout.addWidget(canvas)

        central_widget.setLayout(main_layout)

        self.options = QWidget()
        self.options.setParent(None)
        self.options.setWindowTitle('Options')
        self.options.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.fit_button = QPushButton('Fit Axis')
        self.colorbar_checkbox = QCheckBox('Add Colorbar')

        x_min_label = QLabel('x-Axis Min.')
        x_max_label = QLabel('x-Axis Max.')
        y_min_label = QLabel('y-Axis Min.')
        y_max_label = QLabel('y-Axis Max.')
        ticks_label = QLabel('Minor Ticks')
        grid_label = QLabel('Grid Density')

        self.x_min_spinbox = QDoubleSpinBox()
        self.x_min_spinbox.setRange(-10, 3.9)
        self.x_min_spinbox.setSingleStep(0.1)
        self.x_min_spinbox.setSuffix('  Å^-1')
        self.x_min_spinbox.setValue(-4)
        self.x_min_spinbox.setDecimals(2)

        self.x_max_spinbox = QDoubleSpinBox()
        self.x_max_spinbox.setRange(-3.9, 10)
        self.x_max_spinbox.setSingleStep(0.1)
        self.x_max_spinbox.setSuffix('  Å^-1')
        self.x_max_spinbox.setValue(4)
        self.x_max_spinbox.setDecimals(2)

        self.y_min_spinbox = QDoubleSpinBox()
        self.y_min_spinbox.setRange(-10, 3.9)
        self.y_min_spinbox.setSingleStep(0.1)
        self.y_min_spinbox.setSuffix('  Å^-1')
        self.y_min_spinbox.setValue(-4)
        self.y_min_spinbox.setDecimals(2)

        self.y_max_spinbox = QDoubleSpinBox()
        self.y_max_spinbox.setRange(-3.9, 10)
        self.y_max_spinbox.setSingleStep(0.1)
        self.y_max_spinbox.setSuffix('  Å^-1')
        self.y_max_spinbox.setValue(4)
        self.y_max_spinbox.setDecimals(2)

        self.ticks_spinbox = QSpinBox()
        self.ticks_spinbox.setRange(0, 20)
        self.ticks_spinbox.setSingleStep(1)
        self.ticks_spinbox.setValue(5)

        self.grid_combobox = QComboBox()
        self.grid_combobox.addItem('No Grid')
        self.grid_combobox.addItem('Major Only')
        self.grid_combobox.addItem('Major and Minor')

        options_layout = QGridLayout()

        options_layout.addWidget(self.colorbar_checkbox, 0, 0)
        options_layout.addWidget(x_min_label, 1, 0)
        options_layout.addWidget(x_max_label, 2, 0)
        options_layout.addWidget(y_min_label, 3, 0)
        options_layout.addWidget(y_max_label, 4, 0)
        options_layout.addWidget(ticks_label, 5, 0)
        options_layout.addWidget(grid_label, 6, 0)

        options_layout.addWidget(self.fit_button, 0, 1)
        options_layout.addWidget(self.x_min_spinbox, 1, 1)
        options_layout.addWidget(self.x_max_spinbox, 2, 1)
        options_layout.addWidget(self.y_min_spinbox, 3, 1)
        options_layout.addWidget(self.y_max_spinbox, 4, 1)
        options_layout.addWidget(self.ticks_spinbox, 5, 1)
        options_layout.addWidget(self.grid_combobox, 6, 1)

        self.options.setLayout(options_layout)

        self.options.setFixedSize(options_layout.sizeHint())

    def _initialize_connections(self):

        # Check that max is greater than min
        self.x_min_spinbox.valueChanged.connect(self._update_boundaries)
        self.x_max_spinbox.valueChanged.connect(self._update_boundaries)
        self.y_min_spinbox.valueChanged.connect(self._update_boundaries)
        self.y_max_spinbox.valueChanged.connect(self._update_boundaries)

        self.x_min_spinbox.valueChanged.connect(self.update_axes)
        self.x_max_spinbox.valueChanged.connect(self.update_axes)
        self.y_min_spinbox.valueChanged.connect(self.update_axes)
        self.y_max_spinbox.valueChanged.connect(self.update_axes)
        self.ticks_spinbox.valueChanged.connect(self.update_axes)
        self.grid_combobox.currentIndexChanged.connect(self.update_axes)

        self.fit_button.clicked.connect(self.fit_axis_limit)
        self.colorbar_checkbox.stateChanged.connect(self.add_colorbar)
