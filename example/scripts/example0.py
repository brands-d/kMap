# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.orbital import Orbital

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile)    # compute 3D Fourier transform (see Eqs. 6-11)  
                                              
fig, _ax = plt.subplots(2,3)
ax       = _ax.flatten() 
energies = [10,20,30,50,75,100]      # list of selected kinetic energies
for i, E_kin in enumerate(energies):
    homo.get_kmap(E_kin=E_kin)       # compute momentum map for kinetic energy E_kin (Eq. 12)
    homo.plot(ax[i],                 # plot kmap
              title='$E_{kin}=%g (eV)$'%E_kin,
              kxlim=(-4,4),kylim=(-4,4))    

plt.tight_layout()
plt.show()                          # show figure
