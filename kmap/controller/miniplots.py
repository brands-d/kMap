from itertools import chain

import numpy as np
from pyqtgraph import isosurface
from pyqtgraph.opengl import (
    GLGridItem,
    GLLinePlotItem,
    GLMeshItem,
    GLViewWidget,
    MeshData,
)

from kmap.controller.pyqtgraphplot import PyQtGraphPlot
from kmap.library.misc import energy_to_k, get_rotation_axes
from kmap.library.qwidgetsub import FixedSizeWidget


class MiniKSpacePlot(FixedSizeWidget, PyQtGraphPlot):
    def __init__(self, *args, **kwargs):
        width = 250
        self.ratio = 1
        self.ID = None

        super(MiniKSpacePlot, self).__init__(300, 1, *args, **kwargs)
        self._setup()

    def plot(self, plot_data, ID):
        self.ID = ID

        PyQtGraphPlot.plot(self, plot_data)

    def _setup(self):
        PyQtGraphPlot._setup(self)

        self.ui.histogram.hide()
        self.view.showAxis("bottom", show=False)
        self.view.showAxis("left", show=False)
        self.view.showAxis("top", show=False)
        self.view.showAxis("right", show=False)
        self.view.setAspectLocked(lock=True, ratio=self.ratio)


class MiniRealSpacePlot(GLViewWidget):
    def __init__(self, *args, **kwargs):
        self.options = None
        self.grid = None
        self.bonds = []
        self.photon = None
        self.axis = None
        self.photon_parameters = ["p", 45, 0, 0.694]
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

    def set_options(self, options):
        self.options = options
        self._connect()

    def rotate_orbital(self, phi=0, theta=0, psi=0):
        old_axes = get_rotation_axes(*self.orientation[:2])
        new_axes = get_rotation_axes(phi, theta)
        for item in chain(self.bonds, self.mesh):
            # Undo current orientation
            self._rotate_item(item, old_axes, *self.orientation, backward=True)
            # Actuallly rotate to new orientation
            self._rotate_item(item, new_axes, phi, theta, psi, backward=False)

        self.orientation = [phi, theta, psi]

    def rotate_photon(self, polarization="p", alpha=0, beta=0, s_share=0.694):
        if self.photon is not None:
            self.removeItem(self.photon)
            self.photon = None

        self.photon_parameters = [polarization, alpha, beta, s_share]
        self._refresh_photon()

    def refresh_plot(self):
        self._refresh_axis()
        self._refresh_grid()
        self._refresh_bonds()
        self._refresh_photon()
        self._refresh_mesh()

    def reset_camera(self, distance=75, elevation=90, azimuth=-90):
        # View from top
        self.setCameraPosition(distance=distance, elevation=elevation, azimuth=azimuth)

    def toggle_show_grid(self, state):
        if self.grid is not None:
            self.grid.setVisible(state)

    def toggle_show_bonds(self, state):
        if self.bonds:
            for bond in self.bonds:
                bond.setVisible(state)

    def toggle_show_photon(self, state):
        if self.photon is not None:
            self.photon.setVisible(state)

    def toggle_show_mesh(self, state):
        if self.mesh:
            for mesh in self.mesh:
                mesh.setVisible(state)

    def toggle_show_axis(self, state):
        if self.axis is not None:
            for item in self.axis:
                item.setVisible(state)

    def wheelEvent(self, event, *args, **kwargs):
        event.accept()

        super().wheelEvent(event, *args, **kwargs)

    def _refresh_mesh(self):
        if self.mesh:
            for mesh in self.mesh:
                self.removeItem(mesh)

            self.mesh = []

        if self.orbital is None or not self.options.is_show_mesh():
            return

        data = self.orbital.psi["data"]
        plus_mesh = self._get_iso_mesh(data, "red", 1)
        minus_mesh = self._get_iso_mesh(data, "blue", -1)
        self.addItem(plus_mesh)
        self.addItem(minus_mesh)

        self.mesh = [plus_mesh, minus_mesh]

        # Updating the mesh after iso val change would leave it
        # unrotated
        axes = get_rotation_axes(*self.orientation[:2])
        for item in self.mesh:
            self._rotate_item(item, axes, *self.orientation, backward=False)

    def _refresh_bonds(self):
        if self.bonds:
            for bond in self.bonds:
                self.removeItem(bond)

            self.bonds = []

        if self.orbital is None or not self.options.is_show_bonds():
            return

        color = (0.8, 0.8, 0.8, 1)  # light gray

        for bond in self.orbital.get_bonds():
            new_bond = GLLinePlotItem(pos=bond, color=color, width=5, antialias=True)
            self.bonds.append(new_bond)

            self.addItem(new_bond)

    def _refresh_photon(self):
        # Couldn't find the bug without second part of if so I removed
        # it for now
        if self.photon:
            self.removeItem(self.photon)
            self.photon = None

        polarization, alpha, beta, s_share = self.photon_parameters

        if self.orbital is None or not self.options.is_show_photon():
            return

        color = (1, 1, 0.0, 1)  # color for wavy light ray (yellow)
        ray_length = 50  # length of wavy light ray
        amplitude = 5  # amplitude of oscillation
        wavelength = 5  # wavelength of oscillation
        n_points = 200  # number of points along wavy light ray

        alpha = alpha * np.pi / 180
        beta = (180 + beta) * np.pi / 180
        direction = [
            np.sin(alpha) * np.cos(beta),
            np.sin(alpha) * np.sin(beta),
            np.cos(alpha),
        ]

        x0 = np.linspace(0, ray_length * direction[0], n_points)
        y0 = np.linspace(0, ray_length * direction[1], n_points)
        z0 = np.linspace(0, ray_length * direction[2], n_points)
        t = np.linspace(0, ray_length, n_points)

        if polarization == "s":
            pol_1 = [np.sin(beta), -np.cos(beta), 0]
            pol_2 = [0, 0, 0]

        elif polarization == "p":
            pol_1 = [0, 0, 0]
            pol_2 = [
                np.cos(alpha) * np.cos(beta),
                np.cos(alpha) * np.sin(beta),
                -np.sin(alpha),
            ]

        # ... to be updated ...
        elif polarization == "unpolarized":
            pol_1 = [0, 0, 0]
            p_share = 1 - s_share
            pol_2 = [
                s_share * np.sin(beta) + p_share * np.cos(alpha) * np.cos(beta),
                -s_share * np.cos(beta) + p_share * np.cos(alpha) * np.sin(beta),
                -p_share * np.sin(alpha),
            ]

        elif polarization == "C+":
            pol_1 = [np.sin(beta), -np.cos(beta), 0]
            pol_2 = [
                np.cos(alpha) * np.cos(beta),
                np.cos(alpha) * np.sin(beta),
                -np.sin(alpha),
            ]

        elif polarization == "C-":
            pol_1 = [np.sin(beta), -np.cos(beta), 0]
            pol_2 = [
                -np.cos(alpha) * np.cos(beta),
                -np.cos(alpha) * np.sin(beta),
                +np.sin(alpha),
            ]

        # show C+ spiral ... until I have a better idea ...
        elif polarization == "CDAD":
            pol_1 = [np.sin(beta), -np.cos(beta), 0]
            pol_2 = [
                np.cos(alpha) * np.cos(beta),
                np.cos(alpha) * np.sin(beta),
                -np.sin(alpha),
            ]

        dx = amplitude * pol_1[0] * np.cos(
            2 * np.pi * t / wavelength
        ) + amplitude * pol_2[0] * np.sin(2 * np.pi * t / wavelength)
        dy = amplitude * pol_1[1] * np.cos(
            2 * np.pi * t / wavelength
        ) + amplitude * pol_2[1] * np.sin(2 * np.pi * t / wavelength)
        dz = amplitude * pol_1[2] * np.cos(
            2 * np.pi * t / wavelength
        ) + amplitude * pol_2[2] * np.sin(2 * np.pi * t / wavelength)

        pos = np.array([x0 + dx, y0 + dy, z0 + dz]).T

        photon_line = GLLinePlotItem(pos=pos, color=color, width=5, antialias=True)
        photon_line.setGLOptions("translucent")
        self.photon = photon_line
        self.addItem(photon_line)

    def _refresh_axis(self):
        if self.axis is not None:
            for item in self.axis:
                self.removeItem(item)
            self.axis = None

        axes_items = []

        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
        end_points = [[50, 0, 0], [0, 50, 0], [0, 0, 30]]

        for color, end_point in zip(colors, end_points):
            pos = np.array([[0, 0, 0], end_point])
            axis = GLLinePlotItem(pos=pos, color=color, width=3, antialias=True)
            axis.setGLOptions("translucent")
            axes_items.append(axis)

        self.axis = axes_items
        for item in axes_items:
            self.addItem(item)

    def _refresh_grid(self):
        if self.grid is not None:
            self.removeItem(self.grid)
            self.grid = None

        if self.orbital is None or not self.options.is_show_grid():
            return

        self.grid = GLGridItem()
        dx, dy, dz = [self.orbital.psi[key] for key in ["dx", "dy", "dz"]]
        self.grid.scale(1 / dx, 1 / dy, 1 / dz)
        self.addItem(self.grid)

    def _rotate_item(self, item, axes, phi, theta, psi, backward=False):
        if backward:
            # Undo Rotation in reverse order
            item.rotate(psi, axes[2][0], axes[2][1], axes[2][2], local=True)
            item.rotate(theta, axes[1][0], axes[1][1], axes[1][2], local=True)
            item.rotate(phi, axes[0][0], axes[0][1], axes[0][2], local=True)

        else:
            item.rotate(-phi, axes[0][0], axes[0][1], axes[0][2], local=True)
            item.rotate(-theta, axes[1][0], axes[1][1], axes[1][2], local=True)
            item.rotate(-psi, axes[2][0], axes[2][1], axes[2][2], local=True)

    def _get_iso_mesh(self, data, color, sign):
        iso_val = sign * self.options.get_iso_val()
        vertices, faces = isosurface(data, iso_val * data.max())
        nx, ny, nz = data.shape

        # Center Isosurface around Origin
        vertices[:, 0] = vertices[:, 0] - nx / 2
        vertices[:, 1] = vertices[:, 1] - ny / 2
        vertices[:, 2] = vertices[:, 2] - nz / 2

        mesh_data = MeshData(vertexes=vertices, faces=faces)
        colors = np.zeros((mesh_data.faceCount(), 4), dtype=float)
        # Sets color to Red (RGB, 0 = red, 1 = green, 2 = blue)
        if color == "red":
            colors[:, 0] = 1.0
            colors[:, 1] = 0.2
            colors[:, 2] = 0.2

        elif color == "blue":
            colors[:, 0] = 0.2
            colors[:, 1] = 0.2
            colors[:, 2] = 1.0
        # Transparency (I guess)
        colors[:, 3] = 1
        mesh_data.setFaceColors(colors)

        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, shader="edgeHilight")
        mesh.setGLOptions("translucent")

        return mesh

    def _setup(self):
        # Set Fixed Size. Due to some unknown reason subclassing from a
        # second class like FixedSizeWidget while also
        # subclassing from gl.GLViewWidget throws error
        width = 275
        ratio = 1
        height = width * ratio
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

        self.reset_camera()

    def _connect(self):
        self.options.set_camera.connect(self.reset_camera)
        self.options.show_grid_changed.connect(self.toggle_show_grid)
        self.options.show_mesh_changed.connect(self.toggle_show_mesh)
        self.options.show_bonds_changed.connect(self.toggle_show_bonds)
        self.options.show_photon_changed.connect(self.toggle_show_photon)
        self.options.iso_val_changed.connect(self._refresh_mesh)
        self.options.show_axis_changed.connect(self.toggle_show_axis)


class Mini3DKSpacePlot(GLViewWidget):
    def __init__(self, *args, **kwargs):
        self.ID = None
        self.options = None
        self.grid = None
        self.axis = None
        self.hemisphere = None
        self.mesh = None
        self.orbital = None
        self.orientation = [0, 0, 0]
        self.E_kin = 30
        self.V0 = 0

        super(Mini3DKSpacePlot, self).__init__(*args, **kwargs)
        self._setup()

        self.show()

    def set_orbital(self, orbital, ID):
        self.ID = ID
        self.orbital = orbital
        self.orientation = [0, 0, 0]

        self.refresh_plot()

    def set_options(self, options):
        self.options = options
        self._connect()

    def rotate_orbital(self, phi=0, theta=0, psi=0):
        old_axes = get_rotation_axes(*self.orientation[:2])
        new_axes = get_rotation_axes(phi, theta)

        # Undo current orientation
        self._rotate_item(self.mesh, old_axes, *self.orientation, backward=True)
        # Actuallly rotate to new orientation
        self._rotate_item(self.mesh, new_axes, phi, theta, psi, backward=False)

        self.orientation = [phi, theta, psi]

    def change_energy(self, E_kin):
        self.E_kin = E_kin

        self._refresh_hemisphere()

    def change_inner_potential(self, V0):
        self.V0 = V0

        self._refresh_hemisphere()

    def refresh_plot(self):
        self._refresh_axis()
        self._refresh_hemisphere()
        self._refresh_grid()
        self._refresh_mesh()

    def reset_camera(self, distance=75, elevation=90, azimuth=-90):
        # View from top
        self.setCameraPosition(distance=distance, elevation=elevation, azimuth=azimuth)

    def toggle_show_axis(self, state):
        if self.axis is not None:
            for item in self.axis:
                item.setVisible(state)

    def toggle_show_grid(self, state):
        if self.grid is not None:
            self.grid.setVisible(state)

    def toggle_show_hemisphere(self, state):
        if self.hemisphere is not None:
            self.hemisphere.setVisible(state)

    def _refresh_mesh(self):
        if self.mesh is not None:
            self.removeItem(self.mesh)

            self.mesh = None

        if self.orbital is None:
            return

        data = self.orbital.psik["data"]
        self.mesh = self._get_iso_mesh(data)
        self.addItem(self.mesh)

        # Updating the mesh after iso val change would leave it
        # unrotated
        axes = get_rotation_axes(*self.orientation[:2])
        self._rotate_item(self.mesh, axes, *self.orientation, backward=False)

    def wheelEvent(self, event, *args, **kwargs):
        event.accept()

        super().wheelEvent(event, *args, **kwargs)

    def _refresh_hemisphere(self):
        if self.hemisphere is not None:
            self.removeItem(self.hemisphere)
            self.hemisphere = None

        if self.orbital is None or not self.options.is_show_hemisphere():
            return

        k = energy_to_k(self.E_kin)
        kV = energy_to_k(self.E_kin + self.V0)

        kx, ky, kz = [self.orbital.psik[key] for key in ["kx", "ky", "kz"]]
        self.dx, self.dy, self.dz = [kx[1] - kx[0], ky[1] - ky[0], kz[1] - kz[0]]

        # this produces a hemisphere using the GLSurfacePlotItem, however,
        # the resulting hemisphere appears a little ragged at the circular
        # boundary
        # x = np.linspace(-k / self.dx, k / self.dx, 200)
        # y = np.linspace(-k / self.dy, k / self.dy, 200)
        # X, Y = np.meshgrid(x, y)
        # Z = np.sqrt(k**2 / (self.dx * self.dy) - X**2 - Y**2)

        # self.hemisphere = GLSurfacePlotItem(x=x, y=y, z=Z, color=(
        #    0.5, 0.5, 0.5, 0.7), shader='edgeHilight')
        # self.hemisphere.setGLOptions('translucent')

        # NEW method:
        nz = len(kz)
        X, Y, Z = np.meshgrid(kx / self.dx, ky / self.dy, kz[nz // 2 :] / self.dz)
        data = X**2 + Y**2 + ((k / kV) * Z) ** 2
        iso = k**2 / (self.dx * self.dy)
        color = (0.5, 0.5, 0.5, 0.8)
        self.hemisphere = self._get_iso_mesh(data, iso, color, z_shift=False)

        self.addItem(self.hemisphere)

    def _refresh_axis(self):
        if self.axis is not None:
            for item in self.axis:
                self.removeItem(item)
            self.axis = None

        axes_items = []

        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
        end_points = [[40, 0, 0], [0, 40, 0], [0, 0, 40]]

        for color, end_point in zip(colors, end_points):
            pos = np.array([[0, 0, 0], end_point])
            axis = GLLinePlotItem(pos=pos, color=color, width=3, antialias=True)
            axis.setGLOptions("translucent")
            axes_items.append(axis)

        self.axis = axes_items
        for item in axes_items:
            self.addItem(item)

    def _refresh_grid(self):
        if self.grid is not None:
            self.removeItem(self.grid)
            self.grid = None

        if self.orbital is None or not self.options.is_show_grid():
            return

        self.grid = GLGridItem()
        self.grid.setSize(x=8, y=8, z=8)
        self.grid.scale(1 / self.dx, 1 / self.dy, 1 / self.dz)
        self.addItem(self.grid)

    def _rotate_item(self, item, axes, phi, theta, psi, backward=False):
        if backward:
            # Undo Rotation in reverse order
            item.rotate(psi, axes[2][0], axes[2][1], axes[2][2], local=True)
            item.rotate(theta, axes[1][0], axes[1][1], axes[1][2], local=True)
            item.rotate(phi, axes[0][0], axes[0][1], axes[0][2], local=True)

        else:
            item.rotate(-phi, axes[0][0], axes[0][1], axes[0][2], local=True)
            item.rotate(-theta, axes[1][0], axes[1][1], axes[1][2], local=True)
            item.rotate(-psi, axes[2][0], axes[2][1], axes[2][2], local=True)

    def _get_iso_mesh(self, data, iso=None, color=(1, 0.2, 0.2, 1), z_shift=True):
        if iso is None:
            iso_val = self.options.get_iso_val() * data.max()
        else:
            iso_val = iso

        vertices, faces = isosurface(data, iso_val)
        nx, ny, nz = data.shape

        # Center Isosurface around Origin
        vertices[:, 0] = vertices[:, 0] - nx / 2
        vertices[:, 1] = vertices[:, 1] - ny / 2
        if z_shift:
            vertices[:, 2] = vertices[:, 2] - nz / 2

        mesh_data = MeshData(vertexes=vertices, faces=faces)
        colors = np.zeros((mesh_data.faceCount(), 4), dtype=float)
        for idx in range(4):
            colors[:, idx] = color[idx]

        mesh_data.setFaceColors(colors)

        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, shader="edgeHilight")
        mesh.setGLOptions("translucent")

        return mesh

    def _setup(self):
        # Set Fixed Size. Due to some unknown reason subclassing from a
        # second class like FixedSizeWidget while also
        # subclassing from gl.GLViewWidget throws error
        width = 275
        ratio = 1
        height = width * ratio
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

        self.reset_camera()

    def _connect(self):
        self.options.set_camera.connect(self.reset_camera)
        self.options.show_grid_changed.connect(self.toggle_show_grid)
        self.options.show_hemisphere_changed.connect(self.toggle_show_hemisphere)
        self.options.iso_val_changed.connect(self._refresh_mesh)
        self.options.show_axis_changed.connect(self.toggle_show_axis)
