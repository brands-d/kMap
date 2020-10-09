# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt
import numpy as np

# kMap.py Imports
from kmap.library.orbital import Orbital

# Path to data folder; replace with your own
data_path = Path(__file__).parent / Path('../data/')

cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile)    # compute 3D Fourier transform (see Eqs. 6-11)  
                                              
fig, _ax = plt.subplots(2,3)
ax       = _ax.flatten() 
homo.get_kmap(E_kin=20)
homo.plot(ax[0],title='0',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 

homo.get_kmap(E_kin=20,dk=0.1)
homo.plot(ax[1],title='1',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 

homo.get_kmap(E_kin=20,dk=0.2)
homo.plot(ax[2],title='2',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 

kx = np.linspace(-2,2,50)
ky = np.linspace(-2,2,50)
homo.get_kmap(E_kin=30,dk=(kx,ky))
homo.plot(ax[3],title='3',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 

homo.get_kmap(E_kin=20,dk=(kx,ky))
homo.plot(ax[4],title='4',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 

kx = np.linspace(-3,3,20)
ky = np.linspace(-3,3,20)
homo.get_kmap(E_kin=20,dk=(kx,ky))
homo.plot(ax[5],title='5',kxlim=(-3,3),kylim=(-3,3),interpolation='none') 
       

plt.tight_layout()
plt.show()                          # show figure
