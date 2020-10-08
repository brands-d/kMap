# This script demonstrates how kmaps of several orbitals can be used to
# create the datacube Intensity[BE,kx,ky] as SlicedData object (BE = binding energy)
# To this end a list of molecular orbitals is loaded from a list of URLs 
# pointing to the cube files. By using the orbital energies and a given
# energy broadening parameter the data cube is created and can be sliced as desired.

# Python Imports
from pathlib import Path

# Third Party Imports
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# kMap.py Imports
from kmap.library.database import Database
from kmap.library.sliceddata import SlicedData

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

db = Database(data_path / 'molecules.txt')
molecule = db.get_molecule_by_ID(11)  # choose pentacene molecule for testing ...

# set name and select list of orbitals 
name       = 'pentacene'   # set name for SlicedData Object
orbitals   = []
for orbital in molecule.orbitals[2:-4]:
    orbitals.append([orbital.URL,{'energy':orbital.energy,'name':orbital.name}])

# set parameters
parameters =[35.0,  # photon_energy (float): Photon energy in eV.
             0.0,   # fermi_energy (float): Fermi energy in eV
             0.2,   # energy_broadening (float): FWHM of Gaussian energy broadenening in eV
             0.03,  # dk (float): Desired k-resolution in kmap in Angstroem^-1. 
             0,     # phi (float): Euler orientation angle phi in degree. 
             0,     # theta (float): Euler orientation angle phi in degree. 
             0,     # psi (float): Euler orientation angle phi in degree. 
             'no',  # Ak_type (string): Treatment of |A.k|^2: either 'no', 'toroid' or 'NanoESCA'.  
             'p',   # polarization (string): Either 'p', 's', 'C+', 'C-' or 'CDAD'. 
             0,     # alpha (float): Angle of incidence plane in degree. 
             0,     # beta (float): Azimuth of incidence plane in degree.
             'auto',# gamma (float/str): Damping factor for final state in Angstroem^-1. str = 'auto' sets gamma automatically
             'no']  # symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                    #    '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
             
# initialize SlicedData object
print('Loading orbitals ... please wait ...')
kmap_stack = SlicedData.init_from_orbitals(name,orbitals,parameters)  
print('Loading completed. Now preparing data for volume visualization.')

# Prepare data for viewing
data       = np.nan_to_num(kmap_stack.data)
data       = np.moveaxis(data, 0, -1) # move first axis to last axis
data       = np.asarray(data, order='C')
nx, ny, nz = data.shape
dx         = (kmap_stack.axes[1].range[1] - kmap_stack.axes[1].range[0])/(nx - 1)
dy         = (kmap_stack.axes[2].range[1] - kmap_stack.axes[2].range[0])/(ny - 1)
dz         = (kmap_stack.axes[0].range[1] - kmap_stack.axes[0].range[0])/(nz - 1)
x          = np.linspace(kmap_stack.axes[1].range[0], kmap_stack.axes[1].range[1], nx)
y          = np.linspace(kmap_stack.axes[2].range[0], kmap_stack.axes[2].range[1], ny)
z          = np.linspace(kmap_stack.axes[0].range[0], kmap_stack.axes[0].range[1], nz)

# prepare data for volume visualization
nPoints = 256
data     = np.abs(data) # take absolute value
data[:,y>1.0,:] = 0   # for testing: set data zero for all values y>1
np.clip(data, a_min=0, a_max=0.5*data.max(), out=data) # clip data between 0% and 50% of maximum
data     = (nPoints*data/data.max()).astype(np.ubyte) # convert data to byte-array with values ranging from 0 to 255

# define color map
colors = [
    (0,     0,   0,   0),  # red, green, blue, transparency
    (45,    5,  61,  20),
    (84,   42,  55,  40),
    (150,  87,  60,  60),
    (208, 171, 141,  80),
    (255, 255, 255, 100)
]
cmap = pg.ColorMap(pos=np.linspace(0, 1, len(colors)), color=colors)
ctable = cmap.getLookupTable(start=0, stop=1, nPts=nPoints, alpha=True, mode='byte')

# prepare voxel array
voxel = np.empty(data.shape + (4,), dtype=np.ubyte)
voxel[..., 0] = ctable[data,0]  # red
voxel[..., 1] = ctable[data,1]  # green
voxel[..., 2] = ctable[data,2]  # blue
voxel[..., 3] = ctable[data,3]  # transparency

# initialize GLViewWidget()
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle(name)
w.setCameraPosition(distance=100,elevation=90,azimuth=-90)  # view from top

# display grid in (x,y)-plane
g = gl.GLGridItem()
g.scale(1/dx,1/dy,1/dz)
w.addItem(g)

# add coordinate axes object
ax = gl.GLAxisItem()
ax.setSize(10,10,10)
w.addItem(ax)
        
v = gl.GLVolumeItem(voxel,sliceDensity=1, smooth=True)
v.translate(-nx/2,-ny/2,-nz/2)
w.addItem(v)

QtGui.QApplication.instance().exec_()

