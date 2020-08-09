from kmap.config.config import config


class DataSliderModel():

    def __init__(self, data):

        self.slice_keys = ''
        self.key_label = ''
        self.units = ''

        self.read(data)

    def read(self, data):

        # Slice Keys
        self.slice_keys = data.slice_keys

        # Key Labels
        if 'slice_keys' in data.meta_data:
            self.key_label = data.meta_data['slice_keys']

        else:
            self.key_label = config.get_key(
                'sliced_data', 'default_slice_keys')

        # Units
        if 'slice_unit' in data.meta_data:
            self.units = data.meta_data['slice_unit']

        else:
            self.units = config.get_key('sliced_data', 'default_slice_unit')
