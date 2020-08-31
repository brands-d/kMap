import numpy as np

class LMFitTabModel():

    def __init__(self, controller, sliced_data, orbitals):

        self.controller = controller
        self.sliced = sliced_data
        self.orbitals = orbitals

    def get_sliced_plot(self, index, axis):

        self.displayed_slice_data = self.sliced.slice_from_index(index, axis)

        return self.displayed_slice_data

    def get_selected_orbital_plot(self, ID):

        kmap = self.get_orbital_kmap_by_ID(ID)

        return kmap

    def get_orbital_kmap_by_ID(self, ID):

        orbital = self.ID_to_orbital(ID)
        if orbital is None:
            raise IndexError('wrong ID')

        parameters = self.controller.get_parameters(ID)
        # Split of first element
        weight, *other = parameters
        # Get scaled kmap
        kmap = weight * orbital.get_kmap(*other)

        return kmap

    def get_sum_plot(self):

        kmaps = []

        for orbital in self.orbitals:
            ID = orbital.ID
            kmap = self.get_orbital_kmap_by_ID(ID)
            kmaps.append(kmap)

        if kmaps:
            # Sum kmaps
            self.displayed_sum_data = np.nansum(kmaps)

        else:
            self.displayed_sum_data = None

        return self.displayed_sum_data

    def get_residual_plot(self):

        sum_data = self.get_sum_plot()

    def ID_to_orbital(self, ID):

        for orbital in self.orbitals:
            if orbital.ID == ID:
                return orbital

        return None
