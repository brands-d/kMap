# This script reads the HOMO of pentacene from the example/data folder
# and converts the 3D-Fourier transform into an isosurface povray-input file 
# and runs povray for rendering the 3D Fourier .
# 
# dependencies: (1) POV-ray must be installed (http://www.povray.org/)
#               (2) Python package scikit-image: https://scikit-image.org/docs/dev/install.html 

# Python Imports
from pathlib import Path

# kMap.py Imports
from kmap.library.orbital2povray import Orbital2Povray

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path('../data/')
cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
settings = Path('settings_povray.ini') # check out this file for possible rendering options

# add more elements in povray-image
more_stuff = '''
// x-axis
#declare l = 5;
union{
 cylinder {  <0,0,0>,<l,0,0>,0.075 }
 cone     {  <l,0,0>, 0.15, <l+0.5,0,0>,0.0 }
 pigment { rgb<1,1,1>}
}
// y-axis
#declare l = 5;
union{
 cylinder {  <0,0,0>,<0,-l,0>,0.075 }
 cone     {  <0,-l,0>, 0.15, <0,-l-0.5,0>,0.0 }
 pigment { rgb<1,1,1>}
}
// z-axis
#declare l = 7.5;
union{
 cylinder {  <0,0,0>,<0,0,l>,0.075 }
 cone     {  <0,0,l>, 0.15, <0,0,l+0.5>,0.0 }
 pigment { rgb<1,1,1>}
}
// hemisphere
#declare k = 3.0;
difference{
    sphere{0,k}
    sphere{0,k-0.01}// adjust for the thickness you want
    box{<-k-0.1,-k-0.1,-k-0.1>,<k+0.1,k+0.1,0.0>}
    pigment{rgbt<1,0,0,0.5>}
    scale 1
    }
'''

pov  = Orbital2Povray.init_from_cube(cubefile, domain='reciprocal', 
                                           value='real',  # choose 'real' or 'imag' depending on parity of orbital
                                           dk3D=0.12,
                                           settingsfile=settings)

pov.set_camera({'location':'< 16, 3, 8>',
                'look_at':'< 0, 0, 0>', 
                'sky':'<0,0,1>'})
pov.write_povfile('demo3DFT.pov',add_stuff=more_stuff) # write povray-file 
pov.run_povray(executable='povray +W800 +H600')

