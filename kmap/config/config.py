from configparser import ConfigParser
from kmap import __directory__


class Config:

    def __init__(self):

        self._general_settings = ''
        self._logging_settings = ''

    def setup(self):

        self._general_settings = ConfigParser()
        self._general_settings.read(__directory__ + '/config/settings.ini')

        self._logging_settings = ConfigParser()
        self._logging_settings.read(__directory__ + '/config/logging.ini')

    def get_config(self, file='general'):

        if file == 'general':
            return self._general_settings

        elif file == 'logging':
            return self._logging_settings

        else:
            raise NotImplementedError('%s not implemented' % file)

    def get_key(self, group, key, file='general'):

        if file == 'general':
            return self._general_settings[group][key]

        elif file == 'logging':
            return self._logging_settings[group][key]

        else:
            raise NotImplementedError('%s not implemented' % file)

    def set_key(self, group, key, value, file='general'):
        pass


config = Config()
