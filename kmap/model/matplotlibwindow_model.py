from kmap.library.misc import axis_from_range


class MatplotlibImageModel:
    def __init__(self, plot_data):
        self.image = plot_data.data
        self.x, self.y = self._calc_centered_axes(plot_data)

    def _calc_centered_axes(self, plot_data):
        x_step_size = plot_data.step_size[0]
        centered_range = plot_data.range[0] + [-x_step_size / 2, x_step_size / 2]
        x = axis_from_range(centered_range, len(plot_data.x_axis) + 1)

        y_step_size = plot_data.step_size[1]
        centered_range = plot_data.range[1] + [-y_step_size / 2, y_step_size / 2]
        y = axis_from_range(centered_range, len(plot_data.y_axis) + 1)

        return x, y


class MatplotlibLineModel:
    def __init__(self, plot_data):
        self.data = plot_data
