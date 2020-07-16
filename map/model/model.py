import logging
from map.model.sliceddata import SlicedData


class Model():

    def __init__(self):

        self.root_log = logging.getLogger('root')
        self.sliced_data = []
        self._ID_counter = 0

    def load_sliced_data_from_filepath(self, path):

        self.root_log.info('Trying to load: %s' % path)

        try:
            ID = self._get_new_ID()
            self.root_log.debug('Assigning ID: %i' % ID)

            new_data = SlicedData.init_from_hdf5(path, ID)
            self.root_log.info('Sucessful')

        except AttributeError:
            self.root_log.exception(
                'File could not be loaded. Check if file is missing' +
                'any necessary keys. Traceback:')
            return None

        except OSError:
            self.root_log.exception(
                'File could not be loaded. Check if file has the' +
                'proper file extension. Traceback:')
            return None

        self.sliced_data.append(new_data)
        return new_data

    def _get_new_ID(self):

        self._ID_counter = self._ID_counter + 1

        return self._ID_counter
