# Python Imports
from pathlib import Path

# Third Party Imports
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.misc import energy_to_k

### MAIN PROGRAM ######################################################

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

# load data
cubefile = open(data_path / 'bisanthene_HOMO.cube').read()  # read cube-file from file
orbital  = Orbital(cubefile, dk3D=0.15, E_kin_max=150,value='real') 
data     = orbital.psi['data']
dx,dy,dz = orbital.psi['dx'], orbital.psi['dy'], orbital.psi['dz'] 
nx,ny,nz = data.shape
x, y, z  = orbital.psi['x'], orbital.psi['y'], orbital.psi['z']

# define color map
colors = [
    (255,   0,  0, 100),   # red, semi-transparent
    (255, 255, 255,   0),  # white, fully transparent
    (  0,   0, 255, 100)   # blue, semi-transparent
]

# prepare data for volume visualization
nPoints = 256
data_max = data.max()
data = data/data_max    # normalize data
np.clip(data, a_min=-0.3, a_max=0.3, out=data) # clip data between -30% and 30% of maximum
data = (nPoints//2 + nPoints*data).astype(np.ubyte) # convert data to byte-array with values ranging from 0 to 255

# prepare voxel array
cmap = pg.ColorMap(pos=np.linspace(-1, 1, len(colors)), color=colors)
ctable = cmap.getLookupTable(start=-1, stop=1, nPts=nPoints, alpha=True, mode='byte')
voxels = np.empty(data.shape + (4,), dtype=np.ubyte)
voxels[..., 0] = ctable[data,0]
voxels[..., 1] = ctable[data,1]
voxels[..., 2] = ctable[data,2]
voxels[..., 3] = ctable[data,3]

# initialize GLViewWidget()
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('test of GLVolumeItem')
w.setCameraPosition(distance=100)  

# display grid in (x,y)-plane
g = gl.GLGridItem()
g.setSize(x=12,y=12,z=12)
g.scale(1/dx,1/dy,1/dz)
w.addItem(g)

v = gl.GLVolumeItem(voxels, sliceDensity=1, smooth=True)
v.translate(-nx/2,-ny/2,-nz/2)
w.addItem(v)

QtGui.QApplication.instance().exec_()
