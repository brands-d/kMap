# -*- coding: utf-8 -*-
"""
This example uses the isosurface function to convert a scalar field,
here the momentum space orbital from a cube file, into an isosurface
"""
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

cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
orbital  = Orbital(cubefile, dk3D=0.15, E_kin_max=150,value='real') 
data     = orbital.psik['data']
kx,ky,kz = orbital.psik['kx'], orbital.psik['ky'], orbital.psik['kz'] 
dx,dy,dz = kx[1]-kx[0], ky[1]-ky[0], kz[1]-kz[0]
nx,ny,nz = len(kx), len(ky), len(kz)

# initialize GLViewWidget()
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('test')
w.setCameraPosition(distance=100,elevation=90,azimuth=-90)  # view from top

# display grid in (x,y)-plane
g = gl.GLGridItem()
g.setSize(x=8,y=8,z=8)
g.scale(1/dx,1/dy,1/dz)
w.addItem(g)

# add coordinate axes object
#ax = gl.GLAxisItem()
#ax.setSize(5,5,5)
#w.addItem(ax)

# compute isosurface for positive and negative isovalues
isovals = [+0.2*data.max(), -0.2*data.max()]
colors  = [(1,0.2,0.2), (0.2,0.2,1)]

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
 
# add hemisphere for a given kinetic energy
E_kin = 35.0
k = energy_to_k(E_kin)    

#x = np.linspace(-k/dx, k/dx, 200)
#y = np.linspace(-k/dy, k/dy, 200)
#X,Y = np.meshgrid(x,y)
#Z = np.sqrt(k**2/(dx*dy) - X**2 - Y**2)
#hemisphere = gl.GLSurfacePlotItem(x=x, y=y, z=Z, color=(0.5, 0.5, 0.5, 0.7), shader='edgeHilight')

x = np.linspace(kx[0]/dx, kx[-1]/dx, nx)
y = np.linspace(ky[0]/dy, ky[-1]/dy, ny)
z = np.linspace(    0,    kz[-1]/dz, nz//2)
X, Y, Z = np.meshgrid(x,y,z)
scalar_field = X**2 + Y**2 + Z**2
isoval = k**2/(dx*dy)
color = (0.5, 0.5, 0.5, 0.8)
verts, faces = pg.isosurface(scalar_field, isoval)
verts[:,0] = verts[:,0] - nx/2
verts[:,1] = verts[:,1] - ny/2
verts[:,2] = verts[:,2] 

isosurface = gl.MeshData(vertexes=verts, faces=faces)
rgbt = np.zeros((isosurface.faceCount(), 4), dtype=float)
for c in range(3):
    rgbt[:,c] = color[c] 
rgbt[:,3] = color[3]  # transparency (I guess)
isosurface.setFaceColors(rgbt)

hemisphere = gl.GLMeshItem(meshdata=isosurface, smooth=True,shader='edgeHilight')   
hemisphere.setGLOptions('translucent')
w.addItem(hemisphere)


QtGui.QApplication.instance().exec_()



