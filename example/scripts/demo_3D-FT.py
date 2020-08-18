# -*- coding: utf-8 -*-
"""
This example uses the isosurface function to convert a scalar field,
here the momentum space orbital from a cube file, into an isosurface
"""
import os, sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path + os.sep + '..' + os.sep + '..' + os.sep)
data_path = path + os.sep + '..' + os.sep + 'data' + os.sep
#####

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# local imports 
from kmap.library.orbital import Orbital


### MAIN PROGRAM ######################################################
cubefile = open(data_path + 'pentacene_HOMO.cube').read()  # read cube-file from file
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
g.scale(1/dx,1/dy,1/dz)
w.addItem(g)

# add coordinate axes object
ax = gl.GLAxisItem()
ax.setSize(10,10,10)
w.addItem(ax)

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
        

QtGui.QApplication.instance().exec_()



