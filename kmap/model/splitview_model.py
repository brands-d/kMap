from kmap.library.misc import split_view


class SplitViewTabModel:
    def __init__(self, sliced_data_tab, orbital_data_tab, interpolation):
        self.sliced_data_tab = sliced_data_tab
        self.orbital_data_tab = orbital_data_tab
        self.interpolation = interpolation
        self.displayed_sliced_data = None
        self.displayed_plot_data = None
        self.symmetry = ["no", False]
        self.scale = 1
        self.split_type = "Left Right"

        self.update_displayed_plot_data(0, 0)

    def set_scale(self, scale):
        self.scale = scale

    def set_type(self, type_):
        self.split_type = type_

    def change_symmetry(self, symmetry, mirror):
        self.symmetry = [symmetry, mirror]

    def get_sliced_data(self):
        return self.sliced_data_tab.get_data()

    def update_displayed_plot_data(self, index, axis):
        temp = self.get_sliced_data().slice_from_index(index, axis).copy()
        temp = self.interpolation.interpolate(temp)
        sliced_data = self.interpolation.smooth(temp)
        sliced_data = sliced_data.symmetrise(*self.symmetry)

        temp = self.orbital_data_tab.get_displayed_plot_data().copy()
        temp = self.interpolation.interpolate(temp)
        orbital_data = self.interpolation.smooth(temp)

        self.displayed_plot_data = split_view(
            sliced_data, orbital_data, type_=self.split_type, scale=self.scale
        )

        return self.displayed_plot_data
