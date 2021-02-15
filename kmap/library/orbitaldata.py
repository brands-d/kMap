import os
import urllib.request
from kmap.library.orbital import Orbital
from kmap.config.config import config
from kmap.library.abstractdata import AbstractData


class OrbitalData(Orbital, AbstractData):

    def __init__(self, cube, ID, name='', meta_data={}):

        self.dk3D = float(config.get_key('orbital', 'dk3D'))

        AbstractData.__init__(self, ID, name, meta_data)
        Orbital.__init__(self, cube, file_format='cube', dk3D=self.dk3D,
                         value='abs2')

    @classmethod
    def init_from_file(cls, file_path, ID):
        with open(file_path, 'r') as f:
            file = f.read()

            name, keys = OrbitalData._get_metadata(file, file_path)

        return cls(file, ID, name=name, meta_data=keys)

    @classmethod
    def init_from_online(cls, url, ID, meta_data={}):

        with urllib.request.urlopen(url) as f:
            file = f.read().decode('utf-8')

            name, keys = OrbitalData._get_metadata(file, url)
            name = meta_data['name'] if 'name' in meta_data else name
            meta_data.update(keys)
            
              

        return cls(file, ID, name=name, meta_data=meta_data)

    @classmethod
    def _get_metadata(cls, file, file_path):

        first_line, second_line = file.split('\n')[:2]

        name = os.path.splitext(os.path.split(file_path)[1])[0]
        keys = {config.get_key('cube', 'line_one'): first_line.strip(),
                config.get_key('cube', 'line_two'): second_line.strip()}

        return name, keys

    def __str__(self):

        rep = AbstractData.__str__(self)
        rep += '\ndk3D:\t\t%s' % self.dk3D

        return rep
