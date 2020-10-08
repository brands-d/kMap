# Python Imports
from pathlib import Path

# Third Party Imports
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl   # pip install PyOpenGL

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.misc import get_rotation_axes


class Plot3DMolecule():

    def __init__(self, w, orbital, grid=True, photon={}, isoval=1/6):

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
            line = gl.GLLinePlotItem(pos=bond, color=(0.8,0.8,0.8,1), width=5, antialias=True)
            items.append(line)
            w.addItem(line)

        # compute isosurface for positive and negative isovalues
        isovals = [+isoval*data.max(), -isoval*data.max()]
        colors  = [(1,0.2,0.2), (0.2,0.2,1)]  # red and blue

        for iso, color in zip(isovals, colors):
            # compute isosurface and center around origin
            verts, faces = pg.isosurface(data, iso)
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

            items.append(p)

        if 'polarization' in photon:    # display incident photon
            alpha = photon['alpha']*np.pi/180
            beta = (180 + photon['beta'])*np.pi/180
            direction = [np.sin(alpha)*np.cos(beta), np.sin(alpha)*np.sin(beta), np.cos(alpha)]
            polarization = photon['polarization']

            ray_length = 50  # length of wavy light ray
            amplitude = 5    # amplitude of oscillation
            wavelength = 5   # wavelength of oscillation
            n_points = 200    # number of points along wavy light ray

            x0 = np.linspace(0, ray_length*direction[0], n_points)
            y0 = np.linspace(0, ray_length*direction[1], n_points)
            z0 = np.linspace(0, ray_length*direction[2], n_points)
            t  = np.linspace(0, ray_length, n_points)
            
            if polarization == 's':
                pol_1 = [np.sin(beta), -np.cos(beta), 0]
                pol_2 = [0, 0, 0]

            elif polarization == 'p':
                pol_1 = [0, 0, 0]
                pol_2 = [np.cos(alpha)*np.cos(beta), np.cos(alpha)*np.sin(beta),-np.sin(alpha)]

            elif polarization == 'C+':
                pol_1 = [np.sin(beta), -np.cos(beta), 0]
                pol_2 = [np.cos(alpha)*np.cos(beta), np.cos(alpha)*np.sin(beta),-np.sin(alpha)]

            elif polarization == 'C-':
                pol_1 = [np.sin(beta), -np.cos(beta), 0]
                pol_2 = [-np.cos(alpha)*np.cos(beta),-np.cos(alpha)*np.sin(beta),+np.sin(alpha)]

            elif polarization == 'CDAD': # show C+ spiral ... until I have a better idea ...
                pol_1 = [np.sin(beta), -np.cos(beta), 0]
                pol_2 = [np.cos(alpha)*np.cos(beta), np.cos(alpha)*np.sin(beta),-np.sin(alpha)]

            dx = amplitude*pol_1[0]*np.cos(2*np.pi*t/wavelength) + amplitude*pol_2[0]*np.sin(2*np.pi*t/wavelength)
            dy = amplitude*pol_1[1]*np.cos(2*np.pi*t/wavelength) + amplitude*pol_2[1]*np.sin(2*np.pi*t/wavelength)
            dz = amplitude*pol_1[2]*np.cos(2*np.pi*t/wavelength) + amplitude*pol_2[2]*np.sin(2*np.pi*t/wavelength)

            pos = np.array([x0+dx, y0+dy, z0+dz]).T            

            photon_line = gl.GLLinePlotItem(pos=pos, color=(1,1,0.0,1), width=5, antialias=True)
            photon_line.setGLOptions('translucent')
            w.addItem(photon_line)


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
        axes = get_rotation_axes(old_phi,old_theta)
        for item in self.items:
            item.rotate( old_psi,  axes[2][0],axes[2][1],axes[2][2],local=True) # first undo psi-rotation
            item.rotate( old_theta,axes[1][0],axes[1][1],axes[1][2],local=True) # next undo theta-rotation
            item.rotate( old_phi,  axes[0][0],axes[0][1],axes[0][2],local=True) # finally undo phi-rotation

        # now rotate items to new desired orientation
        axes = get_rotation_axes(phi,theta)
        for item in self.items:
            item.rotate(-phi,  axes[0][0],axes[0][1],axes[0][2],local=True) # first do phi-rotation
            item.rotate(-theta,axes[1][0],axes[1][1],axes[1][2],local=True) # next do theta-rotation
            item.rotate(-psi,  axes[2][0],axes[2][1],axes[2][2],local=True) # finally do psi-rotation
                  
        self.phi   = phi
        self.theta = theta
        self.psi   = psi

        return


### MAIN PROGRAM #######################################################

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
molecule = Orbital(cubefile) # Orbital object contains molecular geometry and psi(x,y,z)

# initialize GLViewWidget()
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('test')
w.setCameraPosition(distance=100,elevation=90,azimuth=-90)  # view from top

molecule_view = Plot3DMolecule(w, molecule, 
                photon={'polarization':'C-', 'alpha':45, 'beta': 0})


#xdirection = gl.GLLinePlotItem(pos=np.array([[0,0,0],[20,0,0]]), color=(1,1,1,0.5), width=5, antialias=True)
#w.addItem(xdirection)
#ydirection = gl.GLLinePlotItem(pos=np.array([[0,0,0],[0,20,0]]), color=(1,0,0,0.5), width=5, antialias=True)
#w.addItem(ydirection)


# a few tests to see if the roration works as desired ...
# (note: only last is shown, so uncomment all others)
#molecule_view.rotate_molecule(phi=20,theta= 0,psi= 0)
#molecule_view.rotate_molecule(phi= 0,theta= 0,psi= 0)
#molecule_view.rotate_molecule(phi= 0,theta=40,psi= 0)
#molecule_view.rotate_molecule(phi= 0,theta= 0,psi= 0)
#molecule_view.rotate_molecule(phi=90,theta=20,psi= 0)
#molecule_view.rotate_molecule(phi= 0,theta= 0,psi= 0)
molecule_view.rotate_molecule(phi=0,theta=0,psi=0)
#molecule_view.rotate_molecule(phi= 0,theta= 0,psi= 0)

# ... all these tests were in agreement with the kmaps shown in the kMap GasPhaseSim-Tab!

QtGui.QApplication.instance().exec_()



