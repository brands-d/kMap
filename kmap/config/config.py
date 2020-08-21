import os
from configparser import ConfigParser

from PyQt5.QtCore import QDir

from kmap import __directory__


class Config:

    def __init__(self):

        settings_default = QDir.toNativeSeparators(
            '/config/settings_default.ini')
        settings_user = QDir.toNativeSeparators(
            '/config/settings_user.ini')
        logging_default = QDir.toNativeSeparators(
            '/config/logging_default.ini')
        logging_user = QDir.toNativeSeparators(
            '/config/logging_user.ini')
        shortcut_default = QDir.toNativeSeparators(
            '/config/shortcut_default.ini')
        shortcut_user = QDir.toNativeSeparators(
            '/config/shortcut_user.ini')

        self.path_settings_default = __directory__ + settings_default
        self.path_settings_user = __directory__ + settings_user
        self.path_logging_default = __directory__ + logging_default
        self.path_logging_user = __directory__ + logging_user
        self.path_shortcut_default = __directory__ + shortcut_default
        self.path_shortcut_user = __directory__ + shortcut_user

        self._general_settings = ''
        self._logging_settings = ''
        self._shortcut_settings = ''

    def setup(self):

        self._check_for_user_files()

        self._general_settings = ConfigParser()
        self._general_settings.read(
            [self.path_settings_default, self.path_settings_user])

        self._logging_settings = ConfigParser()
        self._logging_settings.read(
            [self.path_logging_default, self.path_logging_user])

        self._shortcut_settings = ConfigParser()
        self._shortcut_settings.read(
            [self.path_shortcut_default, self.path_shortcut_user])

    def get_config(self, file='general'):

        if file == 'general':
            return self._general_settings

        elif file == 'logging':
            return self._logging_settings

        elif file == 'shortcut':
            return self._shortcut_settings

        else:
            raise NotImplementedError('%s not implemented' % file)

    def get_key(self, group, key, file='general'):

        if file == 'general':
            return self._general_settings[group][key]

        elif file == 'logging':
            return self._logging_settings[group][key]

        elif file == 'shortcut':
            return self._shortcut_settings[group][key]

        else:
            raise NotImplementedError('%s not implemented' % file)

    def set_key(self, group, key, value, file='general'):
        pass

    def _check_for_user_files(self):

        if not os.path.isfile(self.path_settings_user):
            with open(self.path_settings_user, 'w+') as file:
                file.write('; settings_user.ini')

        if not os.path.isfile(self.path_logging_user):
            with open(self.path_logging_user, 'w+') as file:
                file.write('; logging_user.ini')

        if not os.path.isfile(self.path_shortcut_user):
            with open(self.path_shortcut_user, 'w+') as file:
                file.write('; shortcut_user.ini')


config = Config()
