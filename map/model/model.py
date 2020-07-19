import logging
from map.model.sliceddata import SlicedData
from map.model.orbitaldata import OrbitalData


class Model():

    def __init__(self, app):

        self.app = app
        self.sliced_data = []
        self.orbital_data = []
        self._ID_counter = 0

    def load_data_from_filepath(self, path, data_type):

        log = logging.getLogger('root')
        log.debug('Trying to load: %s.' % path)

        new_data = None
        try:
            ID = self._get_new_ID()
            log.debug('Assigning ID: %i.' % ID)

            if data_type == 'hdf5':
                new_data = SlicedData.init_from_hdf5(path, ID)
                self.sliced_data.append(new_data)

            elif data_type == 'cube':
                new_data = OrbitalData.init_from_file(path, ID)
                self.orbital_data.append(new_data)

            else:
                raise NotImplementedError

            log.info('Successfully loaded %s.' % new_data.name)

        except AttributeError:
            log.exception('%s could not be loaded. Check if ' % path +
                          'file is missing any necessary keys. ' +
                          'Traceback:')

        except OSError:
            log.exception('%s could not be loaded. Check if ' % path +
                          'file has the proper file extension. ' +
                          'Traceback:')

        except Exception as e:
            log.exception('%s could not be loaded. Traceback:' % path)

        finally:
            return new_data

    def _get_new_ID(self):

        self._ID_counter = self._ID_counter + 1

        return self._ID_counter

    def remove_data_by_ID(self, ID):

        logging.getLogger('root').debug('Removing data with ID %i.' % ID)

        for data in self.sliced_data:
            if data.ID == ID:
                self.sliced_data.remove(data)
                return

        for data in self.orbital_data:
            if data.ID == ID:
                self.orbital_data.remove(data)
                return

        # All for loops ran through, thus didn't find ID
        raise LookupError('No data with ID %i found' % ID)

    def reload_settings(self):

        self.app.load_settings()
