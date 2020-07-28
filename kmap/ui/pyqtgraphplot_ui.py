from kmap.ui.abstract_ui import AbstractUI


class PyQtGraphPlotUI(AbstractUI):

    def _initialize_content(self):

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        '''
        Enable if deemed necessary
        x_axis = pg.AxisItem('bottom', text='x-axis', units='A',
                             **{'color': '#FFF', 'font-size': '14pt'})
        y_axis = pg.AxisItem('left', text='y-axis', units='A',
                             **{'color': '#FFF', 'font-size': '14pt'})
        x_axis.showLabel(True)
        y_axis.showLabel(True)
        self.plot_item.view.setAxisItems({'bottom': x_axis, 'left': y_axis})'''
