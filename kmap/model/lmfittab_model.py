import numpy as np


class LMFitTabModel:
    def __init__(self, sliced_data, orbitals):
        self.sliced = sliced_data
        self.orbitals = orbitals
        self.displayed_slice_data = None
        self.displayed_sum_data = None

    def get_sliced_plot(self, index, axis):
        self.displayed_slice_data = self.sliced.slice_from_index(index, axis)

        return self.displayed_slice_data

    def get_selected_orbital_plot(self, ID, parameters):
        kmap = self.get_orbital_kmap_by_ID(ID, parameters)

        return kmap

    def get_orbital_kmap_by_ID(self, ID, parameters):
        orbital = self.ID_to_orbital(ID)
        if orbital is None:
            raise IndexError("wrong ID")

        weight, *parameters = parameters

        # Get scaled kmap
        kmap = weight * orbital.get_kmap(*parameters)

        return kmap

    def get_sum_plot(self, parameters):
        kmaps = []

        for i, orbital in enumerate(self.orbitals):
            ID = orbital.ID
            kmap = self.get_orbital_kmap_by_ID(ID, parameters[i])
            kmaps.append(kmap)

        if kmaps:
            # Sum kmaps
            self.displayed_sum_data = np.nansum(kmaps)

        else:
            self.displayed_sum_data = None

        return self.displayed_sum_data

    def get_residual_plot(self):
        sum_data = self.get_sum_plot()

        return sum_data

    def ID_to_orbital(self, ID):
        for orbital in self.orbitals:
            if orbital.ID == ID:
                return orbital

        return None
