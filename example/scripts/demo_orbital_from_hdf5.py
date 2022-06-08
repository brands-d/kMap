# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.orbital import Orbital

hdf5_path = '../data/ID_00002.hdf5'  # local hdf5-path
server='143.50.77.12'
port='5002'
moleculeID = 2
orbital_names = ['2P_MO_40', '2P_MO_41', '2P_MO_42', '2P_MO_43']
orbital_numbers = [10, 11, 12, 13]

# read orbitals from local hdf5-file
fig, _ax = plt.subplots(2,2)
ax = _ax.flatten() 
for i, orbital_name in enumerate(orbital_names):
    orbital = Orbital.init_from_local_hdf5(hdf5_path, orbital_name)    
    orbital._write_cube(orbital_name + '.cube') # optionally write cube-files
    orbital.get_kmap(E_kin=30.0)      
    orbital.plot(ax[i], title=orbital_name)    

# read orbitals from remote hdf5-file
fig, _ax2 = plt.subplots(2,2)
ax2 = _ax2.flatten() 
for i, orbital_number in enumerate(orbital_numbers):
    orbital = Orbital.init_from_remote_hdf5(server, port, moleculeID, orbital_number)  
    orbital._write_cube('%s.cube'%orbital_number) # optionally write cube-files  
    orbital.get_kmap(E_kin=30.0)      
    orbital.plot(ax2[i], title=orbital.psi['name'])    

# for testing! load same orbitals extracted from hdf5 as cube-files
fig3, _ax3 = plt.subplots(2,2)
ax3 = _ax3.flatten() 
for i, orbital_name in enumerate(orbital_names):
    cube_file = open(orbital_name + '.cube').read()
    orbital = Orbital(cube_file)    
    orbital.get_kmap(E_kin=30.0)      
    orbital.plot(ax3[i], title=orbital_name)  

plt.show()                                                                
