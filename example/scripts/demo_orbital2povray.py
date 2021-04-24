# This scripts read the HOMO of pentacene from the example/data folder
# and converts it into a povray-input file and runs povray
# for rendering the orbital image.
# 
# dependencies: POV-ray must be installed (http://www.povray.org/)

# Python Imports
from pathlib import Path

# Third Party Imports

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.orbital2povray import Orbital2Povray 

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path('../data/')
cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
orbital = Orbital(cubefile) # Orbital object contains molecular geometry and psi(x,y,z)

settings = Path('/data/pep/git/kMap/kmap/config/settings_povray.ini')
povray = Orbital2Povray(orbital, domain='real', settings=settings)
povray.write_povfile('demo.pov')
povray.run_povray(executable='povray')

