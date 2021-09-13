# This script reads the HOMO of pentacene from the example/data folder
# and converts it into a povray-input file and runs povray
# for rendering the orbital image.
# 
# dependencies: (1) POV-ray must be installed (http://www.povray.org/)
#               (2) Python package scikit-image: https://scikit-image.org/docs/dev/install.html 

# Python Imports
from pathlib import Path

# kMap.py Imports
from orbital2povray import Orbital2Povray 

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path('../data/')
cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
settings = Path('settings_povray.ini') # check out this file for possible rendering options

# read in cube file an create POV-ray object
povray = Orbital2Povray.init_from_cube(cubefile, domain='real', settingsfile=settings)

# for demosntration purposes make a copy of the POV-ray object
povray2 = povray.copy()

# rotate and translate molecule in povray-object
povray.rotate(90, 45, 90)  # Use Euler angles theta, phi, psi for rotation
povray.translate([-8, 0, 0])

# write POV-ray input files
povray.write_povfile('demo.pov')
povray2.write_povfile('demo.pov', append=True) #use append to avoid writing header twice

# now run POV-ray to render the image
povray.run_povray(executable='povray')

