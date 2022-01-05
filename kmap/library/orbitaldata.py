import os
import logging
import urllib.request
from pathlib import Path
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
    def init_from_file(cls, path, ID):
        log = logging.getLogger('kmap')
        possible_paths = [path]
        file_name = Path(path).name
        possible_paths.append(Path(config.get_key('paths', 'cube_start')) /
                file_name)
        for path in config.get_key('paths', 'path').split(','):
            possible_paths.append(Path(path) / file_name)

        for path in possible_paths:
            log.info(f'Looking for {file_name} in {path}.')
            if os.path.isfile(path):
                log.info(f'Found.')
                with open(path, 'r') as f:
                    file = f.read()
               
                name, keys = OrbitalData._get_metadata(file, path)
                return cls(file, ID, name=name, meta_data=keys)
            else:
                continue

        print(f'ERROR: File {file_name} wasn\'t found. Please add its location to the search path (general_settings.paths.path')

    @classmethod
    def init_from_online(cls, url, ID, meta_data={}):
        
        log = logging.getLogger('kmap')
        cache_dir = Path(config.get_key('paths', 'cache'))
        cache_file = url.split('OrganicMolecule/')[1].replace('/', '_')
        cache_file = str(cache_dir / cache_file)

        if os.path.isfile(cache_file):
            log.info(f'Found file {url} in cache.')
            with open(cache_file, 'r') as f:
                file = f.read()
                
        else:
            log.info('Loading from database: %s' % url)
            with urllib.request.urlopen(url) as f:
                file = f.read().decode('utf-8')

                if os.path.isdir(cache_dir):
                    log.info(f'Putting {url} into cache {cache_file}')
                    with open(cache_file, 'w') as f:
                        f.write(file)

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
