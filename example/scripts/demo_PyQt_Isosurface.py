# -*- coding: utf-8 -*-
"""
This example uses the isosurface function to convert a scalar field,
here the real space orbital from a cube file, into an isosurface
"""

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# local imports (first include the parent path access kmap-modules)
import os,sys,inspect

from kmap.library.orbital import Orbital

path = os.path.dirname(os.path.realpath(__file__)) + '/../data/'

class Plot3DMolecule():

    def __init__(self, w, orbital, grid=True, isoval=1/6):

        data     = orbital.psi['data']
        dx,dy,dz = orbital.psi['dx'], orbital.psi['dy'], orbital.psi['dz'] 
        nx,ny,nz = data.shape
        bonds    = orbital.get_bonds()

        if grid:    # display grid in (x,y)-plane
            g = gl.GLGridItem()
            g.scale(1/dx,1/dy,1/dz)
            w.addItem(g)

        items  = [] # initialize list of plot items for later rotation

        # add coordinate axes object
        ax = gl.GLAxisItem()
        ax.setSize(10,10,10)
        items.append(ax)
        w.addItem(ax)

        # add bonds as LinePlotItems
        for bond in bonds:
            line = gl.GLLinePlotItem(pos=bond, color=(0.5,1,0.5,0.5), width=5, antialias=True)
            items.append(line)
            w.addItem(line)

        # compute isosurface for positive isovalue
        verts, faces = pg.isosurface(data, isoval*data.max())

        # center isosurface around origin
        verts[:,0] = verts[:,0] - nx/2
        verts[:,1] = verts[:,1] - ny/2
        verts[:,2] = verts[:,2] - nz/2

        plus = gl.MeshData(vertexes=verts, faces=faces)
        colors = np.zeros((plus.faceCount(), 4), dtype=float)
        colors[:,0] = 0.5  # sets color to red (RGB, 0 = red, 1 = green, 2 = blue)
        colors[:,3] = 0.5  # transparency (I guess)
        plus.setFaceColors(colors)

        p = gl.GLMeshItem(meshdata=plus, smooth=True, shader='balloon')
        p.setGLOptions('translucent')  # choose between 'opaque', 'translucent' or 'additive'
        w.addItem(p)
        items.append(p)

        # compute isosurface for negative isovalue  
        verts, faces = pg.isosurface(data,-isoval*data.max())

        # center isosurface around origin
        verts[:,0] = verts[:,0] - nx/2
        verts[:,1] = verts[:,1] - ny/2
        verts[:,2] = verts[:,2] - nz/2

        minus = gl.MeshData(vertexes=verts, faces=faces)
        colors = np.zeros((minus.faceCount(), 4), dtype=float)
        colors[:,2] = 0.5 # sets color to blue (RGB, 0 = red, 1 = green, 2 = blue)
        colors[:,3] = 0.5
        minus.setFaceColors(colors)

        m = gl.GLMeshItem(meshdata=minus, smooth=True, shader='balloon')
        m.setGLOptions('translucent') # choose between 'opaque', 'translucent' or 'additive'
        w.addItem(m)
        items.append(m)

        self.items = items
        self.phi   = 0
        self.theta = 0
        self.psi   = 0

        return 


    def rotate_molecule(self,phi=0,theta=0,psi=0): # Rotate using Euler angles phi, theta, psi
        old_phi   = self.phi
        old_theta = self.theta
        old_psi   = self.psi

        # first rotate items back to original orientation
        axes = self.get_rotation_axes(old_phi,old_theta)
        for item in self.items:
            item.rotate(-old_psi,  axes[2][0],axes[2][1],axes[2][2],local=True) # first undo psi-rotation
            item.rotate( old_theta,axes[1][0],axes[1][1],axes[1][2],local=True) # next undo theta-rotation
            item.rotate(-old_phi,  axes[0][0],axes[0][1],axes[0][2],local=True) # finally undo phi-rotation

        # now rotate items to new desired orientation
        axes = self.get_rotation_axes(phi,theta)
        for item in self.items:
            item.rotate( phi,  axes[0][0],axes[0][1],axes[0][2],local=True) # first do phi-rotation
            item.rotate(-theta,axes[1][0],axes[1][1],axes[1][2],local=True) # next do theta-rotation
            item.rotate( psi,  axes[2][0],axes[2][1],axes[2][2],local=True) # finally do psi-rotation
                  
        self.phi   = phi
        self.theta = theta
        self.psi   = psi

        return

    def get_rotation_axes(self,phi,theta):

        deg2rad   = np.pi/180
        cos_phi   = np.cos(phi*deg2rad)
        sin_phi   = np.sin(phi*deg2rad)
        cos_theta = np.cos(theta*deg2rad)
        sin_theta = np.sin(theta*deg2rad)

        axis1   = [0,0,1]  # first axis is always the z-axis
        axis2   = [cos_phi,-sin_phi, 0]  # x' axis
        axis3   = [-sin_phi*sin_theta, -cos_phi*sin_theta, cos_theta] # z'' axis

        return [axis1, axis2, axis3]

### MAIN PROGRAM ######################################################
cubefile = open(path + 'pentacene_HOMO.cube').read()  # read cube-file from file
molecule = Orbital(cubefile) # Orbital object contains molecular geometry and psi(x,y,z)

# initialize GLViewWidget()
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('test')
w.setCameraPosition(distance=100,elevation=90,azimuth=0)  # view from top

molecule_view = Plot3DMolecule(w, molecule)

# a few tests to see if the roration works as desired ...
# (note: only last is shown, so uncomment all others)
molecule_view.rotate_molecule(phi=90,theta=30)
molecule_view.rotate_molecule(phi=90,theta=0)
molecule_view.rotate_molecule(phi=0,theta=45)
molecule_view.rotate_molecule(phi=90,theta=30)
molecule_view.rotate_molecule(phi=0,theta=0,psi=30)
molecule_view.rotate_molecule(phi=0,theta=0,psi=0)
molecule_view.rotate_molecule(phi=90,theta=30,psi=90)
molecule_view.rotate_molecule(phi=0,theta=0,psi=0)
# ... all these tests were in agreement with the kmaps shown in the kMap GasPhaseSim-Tab!

QtGui.QApplication.instance().exec_()



