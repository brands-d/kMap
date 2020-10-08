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
homo     = Orbital(cubefile,        # compute 3D Fourier transform (see Eqs. 6-11)  
                   dk3D=0.15)       # with a desired k-spacing of dkx = dky = dkz = 0.15 1/Angstroem                           

fig, ax = plt.subplots(1,3)         # create empty figure with 3 axes

# plot Figure 3(a): HOMO of pentacene with phi = 30°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=30)               # Euler angle phi = 30            
homo.plot(ax[0])                    # plot kmap in axis 0

# plot Figure 3(b): HOMO of pentacene with phi = 0°, theta = -45°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=0,                # Euler angle phi = 0   
              theta=-45)            # Euler angle theta = -45                 
homo.plot(ax[1])                    # plot kmap in axis 1

# plot Figure 3(c): HOMO of pentacene with phi = 90°, theta = -45°, psi = 60°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=90,               # Euler angle phi = 90   
              theta=-45,            # Euler angle theta = -45  
              psi=60)               # Euler angle psi = 60°               
homo.plot(ax[2])                    # plot kmap in axis 2


plt.tight_layout()
plt.show()                          # show figure
