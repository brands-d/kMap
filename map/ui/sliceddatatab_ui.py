from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox
import pyqtgraph as pg


class SlicedDataTabUI(AbstractUI):

    def _initialize_content(self):

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Plot
        self.plot_item = pg.ImageView(view=pg.PlotItem())
        self.plot_item.view.invertY(False)
        self.plot_item.view.hideButtons()
        self.plot_item.ui.roiBtn.hide()
        self.plot_item.ui.menuBtn.hide()
        '''
        Enable if deemed necessary
        x_axis = pg.AxisItem('bottom', text='x-axis', units='A',
                             **{'color': '#FFF', 'font-size': '14pt'})
        y_axis = pg.AxisItem('left', text='y-axis', units='A',
                             **{'color': '#FFF', 'font-size': '14pt'})
        x_axis.showLabel(True)
        y_axis.showLabel(True)
        self.plot_item.view.setAxisItems({'bottom': x_axis, 'left': y_axis})'''
        main_layout.addWidget(self.plot_item)
