# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.orbital import Orbital

hdf5_path = '../data/ID_00002.hdf5'

fig, _ax = plt.subplots(2,2)
ax = _ax.flatten() 
orbital_names = ['2P_MO_40', '2P_MO_41', '2P_MO_42', '2P_MO_43']

for i, orbital_name in enumerate(orbital_names):
    orbital = Orbital(hdf5_path, file_format='hdf5', orbital_name=orbital_name)    
    orbital._write_cube(orbital_name + '.cube')
    orbital.get_kmap(E_kin=30.0)      
    orbital.plot(ax[i], title=orbital_name)    

# for testing! load same orbitals extracted from hdf5 as cube-files
fig2, _ax2 = plt.subplots(2,2)
ax2 = _ax2.flatten() 
for i, orbital_name in enumerate(orbital_names):
    cube_file = open(orbital_name + '.cube').read()
    orbital = Orbital(cube_file)    
    orbital.get_kmap(E_kin=30.0)      
    orbital.plot(ax2[i], title=orbital_name)  

plt.show()                                                                
