# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
#from kmap.library.orbital import Orbital
from kmap.library.orbital import Orbital

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

cubefile = open(data_path / 'C60_MO_180.cube').read()  # read cube-file from file
#cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile)    # compute 3D Fourier transform (see Eqs. 6-11)  
                                              
fig, _ax = plt.subplots(3,3)
ax       = _ax.flatten() 
E_kin = 30.0
V0_list = [0, 2, 4, 6, 8, 10, 12, 14, 16]      # list of selected inner potential values
for i, V0 in enumerate(V0_list):
    homo.get_kmap(E_kin=E_kin, V0=V0)       # compute momentum map for kinetic energy E_kin (Eq. 12)
    homo.plot(ax[i],                 # plot kmap
              title='$E_{kin}=%g$ eV, $V_0=%g$ eV'%(E_kin, V0),
              kxlim=(-3,3),kylim=(-3,3))    

plt.tight_layout()
plt.show()                          # show figure
