# This script demonstrates how kmaps of several orbitals can be used to
# create the datacube Intensity[BE,kx,ky] as SlicedData object (BE = binding energy)
# To this end a list of molecular orbitals is loaded from a list of URLs 
# pointing to the cube files. By using the orbital energies and a given
# energy broadening parameter the data cube is created and can be sliced as desired.

# Python imports
import os, sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path + os.sep + '..' + os.sep + '..' + os.sep)
data_path = path + os.sep + '..' + os.sep + 'data' + os.sep

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# kmap imports
from kmap.library.database import Database
from kmap.library.sliceddata import SlicedData

# 
db = Database(data_path + 'molecules.txt')
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
kmap_stack = SlicedData.init_from_orbitals(name,orbitals,parameters)  

# Prepare data for viewing
data       = np.nan_to_num(kmap_stack.data)
data       = np.moveaxis(data, 0, -1) # move first axis to last axis
data       = np.asarray(data, order='C')
nx, ny, nz = data.shape
dx         = (kmap_stack.axes[1].range[1] - kmap_stack.axes[1].range[0])/(nx - 1)
dy         = (kmap_stack.axes[2].range[1] - kmap_stack.axes[2].range[0])/(ny - 1)
dz         = (kmap_stack.axes[0].range[1] - kmap_stack.axes[0].range[0])/(nz - 1)

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

# compute isosurface for positive and negative isovalues
isovals = [+0.2*data.max()]
colors  = [(1,0.2,0.2)]

for isoval, color in zip(isovals, colors):
    # compute vertices and faces and center around origin
    verts, faces = pg.isosurface(data, isoval)
    verts[:,0] = verts[:,0] - nx/2
    verts[:,1] = verts[:,1] - ny/2
    verts[:,2] = verts[:,2] - nz/2

    isosurface = gl.MeshData(vertexes=verts, faces=faces)
    rgbt = np.zeros((isosurface.faceCount(), 4), dtype=float)
    for c in range(3):
        rgbt[:,c] = color[c] 
    rgbt[:,3] = 1  # transparency (I guess)
    isosurface.setFaceColors(rgbt)

    p = gl.GLMeshItem(meshdata=isosurface, smooth=True, 
                      shader='edgeHilight')   # shader options: 'balloon', 'shaded', 'normalColor', 'edgeHilight'
    p.setGLOptions('translucent')  # choose between 'opaque', 'translucent' or 'additive'
    w.addItem(p)
        

QtGui.QApplication.instance().exec_()

