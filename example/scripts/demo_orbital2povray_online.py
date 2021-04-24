# This scripts downloads the HOMO and LUMO orbitals of bisanthene 
# from the online molecule database (ID=406) http://143.50.77.12:5000/
# It converts the cube-files into povray-input files and runs povray
# for rendering orbital images.
# 
# dependencies: POV-ray must be installed (http://www.povray.org/)
#
# Python Imports
from pathlib import Path
import urllib.request

# Third Party Imports

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.database import Database
from kmap.library.orbital2povray import Orbital2Povray 

# set path to your molecules.txt file from the kMap.py installation
molecules_path = '/data/pep/git/kMap/kmap/resources/misc/molecules.txt'
# set path to povray settings file
settings = Path('/data/pep/git/kMap/kmap/config/settings_povray.ini')

ID = 406 # choose molecule ID from database

########################################################
db = Database(molecules_path)
molecule = db.get_molecule_by_ID(ID)
chosen_orbitals = ['HOMO', 'LUMO']  # give list of orbitals or set choose_orbitals = 'all'

for orbital in molecule.orbitals:
    name = orbital.name.split()[-1]
    if type(chosen_orbitals) == str or name in chosen_orbitals:
        with urllib.request.urlopen(orbital.URL) as f:
            file = f.read().decode('utf-8')  # read cube from online-database
            orbital_data = Orbital(file) # create Orbital object
            povray = Orbital2Povray(orbital_data, domain='real', settings=settings) # convert to povray
            povray.write_povfile('%04i_%s.pov'%(ID, name)) # write povray-file 
            povray.run_povray(executable='povray')

