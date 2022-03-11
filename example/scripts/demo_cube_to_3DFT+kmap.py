# Python Imports
from pathlib import Path

# For a chosen molecule with the ID
ID = 406
# an orbital 
orbital_name = 'HOMO-9'
# this script downloads the cube file from the molecule database http://143.50.77.12:5000/
# and then uses orbital2povray to render three-dimensional plots of the orbital
# in real space and in momentum space using 'povray' with this settings:
settings = Path('white_settings.ini') 
# For the momentum space plot, the script also displays
# a hemishpere corresponding to the kinetic energy
E_kin = 60
# Note that the angle 
phi = 90
# is used to rotate the molecule (real and momentum space) along the z-axis.
# Finally , also a 2D-momentum map corresponding to the chosen kinetic energy
# is plotted

# dependencies: (1) POV-ray must be installed (http://www.povray.org/)
#               (2) Python package scikit-image: https://scikit-image.org/docs/dev/install.html 


# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

# kMap.py Imports
from kmap.library.database import Database
from kmap.library.orbital import Orbital
from kmap.library.misc import energy_to_k
from kmap.library.orbital2povray import Orbital2Povray

# here are other possible choices
#E_kin = 30; ID = 406; orbital_name = 'HOMO';  # bisanthene (gas phase geometry) PBE-GGA, 
#E_kin = 30; ID = 406; orbital_name = 'LUMO';  # bisanthene (gas phase geometry) PBE-GGA, 
#E_kin = 60; ID = 406; orbital_name = 'HOMO-8';# bisanthene (gas phase geometry) PBE-GGA, 
#E_kin = 60; ID = 406; orbital_name = 'HOMO-9';# bisanthene (gas phase geometry) PBE-GGA, 
#E_kin = 30; ID = 406; orbital_name = 'HOMO-5';# bisanthene (gas phase geometry) PBE-GGA, 

# define paths and select orbital ID
db = Database('../../kmap/resources/misc/molecules.txt')  # define path to molecules.txt file

# add more elements in povray-image
FT_stuff = '''
// x-axis
#declare l = 5;
union{
 cylinder {  <0,0,0>,<l,0,0>,0.075 }
 cone     {  <l,0,0>, 0.15, <l+0.5,0,0>,0.0 }
 pigment { rgb<0,0,0>}
}
// y-axis
#declare l = 7.5;
union{
 cylinder {  <0,0,0>,<0,-l,0>,0.075 }
 cone     {  <0,-l,0>, 0.15, <0,-l-0.5,0>,0.0 }
 pigment { rgb<0,0,0>}
}
// z-axis
#declare l = 4.5;
union{
 cylinder {  <0,0,0>,<0,0,l>,0.075 }
 cone     {  <0,0,l>, 0.15, <0,0,l+0.5>,0.0 }
 pigment { rgb<0,0,0>}
}
// hemisphere
#declare k = %g;
difference{
    sphere{0,k}
    sphere{0,k-0.01}// adjust for the thickness you want
    box{<-k-0.1,-k-0.1,-k-0.1>,<k+0.1,k+0.1,0.0>}
    pigment{rgbt<1,0,0,0.5>}
    scale 1
    }
'''%(energy_to_k(E_kin))

real_stuff = '''
// x-axis
#declare l = 6;
union{
 cylinder {  <0,0,0>,<l,0,0>,0.075 }
 cone     {  <l,0,0>, 0.15, <l+0.5,0,0>,0.0 }
 pigment { rgb<0,0,0>}
}
// y-axis
#declare l = 7;
union{
 cylinder {  <0,0,0>,<0,-l,0>,0.075 }
 cone     {  <0,-l,0>, 0.15, <0,-l-0.5,0>,0.0 }
 pigment { rgb<0,0,0>}
}
// z-axis
#declare l = 4.0;
union{
 cylinder {  <0,0,0>,<0,0,l>,0.075 }
 cone     {  <0,0,l>, 0.15, <0,0,l+0.5>,0.0 }
 pigment { rgb<0,0,0>}
}
'''

def add_color_bar(im, ax):
    from mpl_toolkits import axes_grid1
    aspect = 20
    pad_fraction = 1.0
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)

    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(ax)
    cb = im.axes.figure.colorbar(im, cax=cax)
    #cax.set_ylabel(r'$|\tilde{\Psi}_i(k_x,k_y)|^2$', fontsize=28)  
    cax.set_ylabel(r'$I_i(k_x,k_y)$', fontsize=28)
    return

# search for chosen orbital
molecule = db.get_molecule_by_ID(ID)  # 
for cube_data in molecule.orbitals:
    if cube_data.name[-len(orbital_name):] == orbital_name: break

# check symmetry of orbital and choose real or imaginary part for 3D-FT
if cube_data.symmetry[-1] == 'g':  # even
    value = 'real'

elif cube_data.symmetry[-1] == 'u':  # odd
    value = 'imag'

else:
    value = 'abs'   # otherwise take absolute value
    

# load cubefile of chosen orbital from online-database
with urllib.request.urlopen(cube_data.URL) as f:
    cubefile = f.read().decode('utf-8') 


for domain in ['real', 'reciprocal']:

    if domain == 'reciprocal':
        pov = Orbital2Povray.init_from_cube(cubefile, domain='reciprocal', 
                                                  value=value,
                                                  dk3D=0.10,
                                                  settingsfile=settings)
    else:
        pov = Orbital2Povray.init_from_cube(cubefile, domain='real', 
                                                  settingsfile=settings)

    pov.rotate(phi, 0, 0)  # Use Euler angles theta, phi, psi for rotation
    #pov.translate([0, 0, 0])
    pov.set_camera({'location':'<5.0,8.0, 7.0>','look_at':'<0.0,0.0,0.0>'})

    # write povray-files
    if domain == 'reciprocal':
        povname = 'ID%i_%s_3DFT.pov'%(ID, orbital_name)
        pov.write_povfile(povname, add_stuff=FT_stuff) # use append to avoid writing header twice

    else:
        povname = 'ID%i_%s.pov'%(ID, orbital_name)
        pov.write_povfile(povname, add_stuff=real_stuff) # use append to avoid writing header twice

    pov.run_povray(executable='povray +W1600 +H1200')


# now compute 2D-momentum map
orbital = Orbital(cubefile, dk3D=0.10, E_kin_max=80)    # compute 3D Fourier transform (see Eqs. 6-11)  
orbital.get_kmap(E_kin=E_kin, Ak_type='no', phi=phi, polarization='p', alpha=45)   # compute momentum map for kinetic energy E_kin (Eq. 12)
data = orbital.Ak['data']*orbital.kmap['data'] 
data = np.abs(data)

# make plot
krange = orbital.kmap['krange']
limits = [krange[0][0], krange[0][1], krange[1][0], krange[1][1]]

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})
# plot kmap 
fig, ax = plt.subplots(1,1)

im = ax.imshow(data,
                extent=limits,
                interpolation='bicubic',
                origin='lower',
                cmap='afmhot')

# format plot
ax.set_aspect('equal')
ax.set_xlabel(r'$k_x$ (\AA$^{-1}$)', fontsize=22)
ax.set_ylabel(r'$k_y$ (\AA$^{-1}$)', fontsize=22)

ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ticks = np.linspace(-4, +4, 9)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)
add_color_bar(im, ax)
plt.tight_layout()
plt.savefig('ID%i_%s_2DFT.png'%(ID, orbital_name), dpi=300)
plt.show()                      # show figure
