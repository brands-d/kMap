import logging
import os
import urllib.request
from pathlib import Path

import h5py

from kmap.config.config import config
from kmap.library.abstractdata import AbstractData
from kmap.library.misc import get_remote_hdf5_orbital, write_cube
from kmap.library.orbital import Orbital


class OrbitalData(Orbital, AbstractData):
    def __init__(self, data, ID, name="", meta_data={}, file_format="cube"):
        self.dk3D = float(config.get_key("orbital", "dk3D"))

        AbstractData.__init__(self, ID, name, meta_data)
        Orbital.__init__(
            self,
            data,
            file_format=file_format,
            dk3D=self.dk3D,
            value="abs2",
            orbital_name=name,
        )

    @classmethod
    def init_from_file(cls, path, ID):
        log = logging.getLogger("kmap")
        possible_paths = [path]
        file_name = Path(path).name
        possible_paths.append(Path(config.get_key("paths", "cube_start")) / file_name)
        for path in config.get_key("paths", "path").split(","):
            possible_paths.append(Path(path) / file_name)

        for path in possible_paths:
            log.info(f"Looking for {file_name} in {path}.")
            if os.path.isfile(path):
                log.info(f"Found.")
                with open(path, "r") as f:
                    file = f.read()

                name, keys = OrbitalData._get_metadata(file, path)
                return cls(file, ID, name=name, meta_data=keys)
            else:
                continue

        print(
            f"ERROR: File {file_name} wasn't found. Please add its location to the search path (general_settings.paths.path"
        )

    @classmethod
    def init_from_online(cls, url, ID, meta_data={}):
        log = logging.getLogger("kmap")
        cache_dir = Path(config.get_key("paths", "cache"))
        cache_file = url.split("cubefiles/")[1].replace("/", "_")
        cache_file = str(cache_dir / cache_file)

        if os.path.isfile(cache_file):
            log.info(f"Found file {url} in cache.")
            with open(cache_file, "r") as f:
                file = f.read()

            name, keys = OrbitalData._get_metadata(file, url)
            name = meta_data["name"] if "name" in meta_data else name
            meta_data.update(keys)
            file_format = "cube"

        else:
            try:
                log.info(f'Loading from ID{meta_data["ID"]:05d} hdf5 file....')
                molecule, psi = get_remote_hdf5_orbital(
                    "143.50.187.12",
                    "80",
                    int(float(meta_data["database ID"])),
                    int(meta_data["ID"]) - 1,
                )

                if os.path.isdir(cache_dir):
                    log.info(f"Putting {url} into cache {cache_file}")
                    write_cube(psi, molecule, cache_file)

                file = h5py.File("aux.hdf5", "w", driver="core", backing_store=False)
                file.create_dataset("num_atom", data=molecule["num_atom"])
                file.create_dataset(
                    "chemical_numbers", data=molecule["chemical_numbers"]
                )
                file.create_dataset(
                    "atomic_coordinates",
                    data=molecule["atomic_coordinates"],
                    dtype="float64",
                )
                file.create_dataset("x", data=psi["x"], dtype="float64")
                file.create_dataset("y", data=psi["y"], dtype="float64")
                file.create_dataset("z", data=psi["z"], dtype="float64")
                file.create_dataset("data", data=psi["data"], dtype="float64")
                name = psi["name"]
                file_format = "hdf5"

            except:
                log.info("HDF5 File not available, loading cube file...")
                log.info("Loading from database: %s" % url)
                with urllib.request.urlopen(url) as f:
                    file = f.read().decode("utf-8")

                    if os.path.isdir(cache_dir):
                        log.info(f"Putting {url} into cache {cache_file}")
                        with open(cache_file, "w") as f:
                            f.write(file)

                name, keys = OrbitalData._get_metadata(file, url)
                name = meta_data["name"] if "name" in meta_data else name
                meta_data.update(keys)
                file_format = "cube"

        return cls(file, ID, name=name, meta_data=meta_data, file_format=file_format)

    @classmethod
    def _get_metadata(cls, file, file_path):
        first_line, second_line = file.split("\n")[:2]

        name = os.path.splitext(os.path.split(file_path)[1])[0]
        keys = {
            config.get_key("cube", "line_one"): first_line.strip(),
            config.get_key("cube", "line_two"): second_line.strip(),
        }

        return name, keys

    def __str__(self):
        rep = AbstractData.__str__(self)
        rep += "\ndk3D:\t\t%s" % self.dk3D

        return rep
