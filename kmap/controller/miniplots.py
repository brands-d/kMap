from itertools import chain
import numpy as np

from pyqtgraph.opengl import (
    GLViewWidget, GLGridItem, GLLinePlotItem, MeshData, GLMeshItem)
from pyqtgraph import isosurface

from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.library.qwidgetsub import FixedSizeWidget
from kmap.library.misc import get_rotation_axes


class MiniKSpacePlot(FixedSizeWidget, PyQtGraphPlot):

    def __init__(self, *args, **kwargs):

        width = 300
        self.ratio = 1
        self.ID = None

        super(MiniKSpacePlot, self).__init__(300, 1, *args, **kwargs)

    def plot(self, plot_data, ID):

        self.ID = ID

        PyQtGraphPlot.plot(self, plot_data)

    def _setup(self):

        PyQtGraphPlot._setup(self)

        self.ui.histogram.hide()
        self.view.showAxis('bottom', show=True)
        self.view.showAxis('left', show=True)
        self.view.showAxis('top', show=True)
        self.view.showAxis('right', show=True)
        self.view.setAspectLocked(lock=True, ratio=self.ratio)


class MiniRealSpacePlot(GLViewWidget):

    def __init__(self, *args, grid=True, iso_val=1 / 6, **kwargs):

        self.show_grid = grid
        self.iso_val = iso_val
        self.grid = None
        self.bonds = []
        self.mesh = []
        self.orbital = None
        self.orientation = [0, 0, 0]

        super(MiniRealSpacePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.show()

    def set_orbital(self, orbital):

        self.orbital = orbital
        self.orientation = [0, 0, 0]

        self.refresh_plot()

    def rotate_orbital(self, phi=0, theta=0, psi=0):

        old_axes = get_rotation_axes(*self.orientation[:2])
        new_axes = get_rotation_axes(phi, theta)
        for item in chain(self.bonds, self.mesh):
            # Undo current orientation
            self._rotate_item(item, old_axes, *self.orientation,
                              backward=True)
            # Actuallly rotate to new orientation
            self._rotate_item(item, new_axes, phi, theta, psi, backward=False)

        self.orientation = [phi, theta, psi]

    def refresh_plot(self):

        self._refresh_grid()
        self._refresh_bonds()
        self._refresh_mesh()

    def mouseMoveEvent(self, event):

        event.ignore()

    def mousePressEvent(self, event):

        event.ignore()

    def mouseReleaseEvent(self, event):

        event.ignore()

    def _refresh_mesh(self):

        if self.mesh:
            for mesh in self.mesh:
                self.removeItem(mesh)

            self.mesh = []

        if self.orbital is None:
            return

        data = self.orbital.psi['data']
        plus_mesh = self._get_iso_mesh(data, 'red', self.iso_val)
        minus_mesh = self._get_iso_mesh(data, 'blue', -self.iso_val)
        self.addItem(plus_mesh)
        self.addItem(minus_mesh)

        self.mesh = [plus_mesh, minus_mesh]

    def _refresh_bonds(self):

        if self.bonds:
            for bond in self.bonds:
                self.removeItem(bond)

            self.bonds = []

        if self.orbital is None:
            return

        color = (0.5, 1, 0.5, 0.5)

        for bond in self.orbital.get_bonds():
            new_bond = GLLinePlotItem(pos=bond, color=color,
                                      width=5, antialias=True)
            self.bonds.append(new_bond)

            self.addItem(new_bond)

    def _refresh_grid(self):

        if self.grid is not None:
            self.removeItem(self.grid)
            self.grid = None

        if self.orbital is None:
            return

        if self.show_grid:
            self.grid = GLGridItem()
            dx, dy, dz = [self.orbital.psi[key] for key in ['dx', 'dy', 'dz']]
            self.grid.scale(1 / dx, 1 / dy, 1 / dz)
            self.addItem(self.grid)

    def _rotate_item(self, item, axes, phi, theta, psi, backward=False):

        if backward:
            # Undo Rotation in reverse order
            item.rotate(-psi, axes[2][0], axes[2][1], axes[2][2], local=True)
            item.rotate(theta, axes[1][0], axes[1][1], axes[1][2], local=True)
            item.rotate(-phi, axes[0][0], axes[0][1], axes[0][2], local=True)

        else:
            item.rotate(phi, axes[0][0], axes[0][1], axes[0][2], local=True)
            item.rotate(-theta, axes[1][0], axes[1][1], axes[1][2],
                        local=True)
            item.rotate(psi, axes[2][0], axes[2][1], axes[2][2], local=True)

    def _get_iso_mesh(self, data, color, iso_val):

        vertices, faces = isosurface(data, iso_val * data.max())
        nx, ny, nz = data.shape

        # Center Isosurface around Origin
        vertices[:, 0] = vertices[:, 0] - nx / 2
        vertices[:, 1] = vertices[:, 1] - ny / 2
        vertices[:, 2] = vertices[:, 2] - nz / 2

        mesh_data = MeshData(vertexes=vertices, faces=faces)
        colors = np.zeros((mesh_data.faceCount(), 4), dtype=float)
        # Sets color to Red (RGB, 0 = red, 1 = green, 2 = blue)
        if color == 'red':
            colors[:, 0] = 0.5

        elif color == 'blue':
            colors[:, 2] = 0.5
        # Transparency (I guess)
        colors[:, 3] = 0.5
        mesh_data.setFaceColors(colors)

        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, shader='balloon')
        mesh.setGLOptions('translucent')

        return mesh

    def _setup(self):

        # View from top
        self.setCameraPosition(distance=75, elevation=90, azimuth=0)

        # Set Fixed Size. Due to some unknown reason subclassing from a
        # second class like FixedSizeWidget while also
        # subclassing from gl.GLViewWidget throws error
        width = 300
        ratio = 1
        height = width * ratio
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)
