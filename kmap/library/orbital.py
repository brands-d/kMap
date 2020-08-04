"""Defines the Orbital class.

This file defines a class named Orbital designed to read, hold,
calculate and slice data from cube files.
"""

import numpy as np
import scipy.interpolate as interp
from kmap.library.plotdata import PlotData

np.seterr(invalid='ignore')

class Orbital():
    """Class modelling cube files as orbitals from which kmaps can be
    sliced.

    This file defines a class named Orbital designed to read, hold,
    calculate and slice data from cube files.

    Args:
        file (string): Entire cube file to be loaded as one string.
        file_format (string): Currently only cube files are supported.
        dk3D (float): Desired resolution for 3D-Fourier-Transform.
            Single number.
        value (string): choose between 'real', 'imag', 'abs' or 'abs2'
            for Re(), Im(), |..| or |..|^2

    Attributes:

    """

    def __init__(self, file, file_format='cube', dk3D=0.15, value='abs2'):

        # Read orbital data from file
        if file_format == 'cube': 
            self._read_cube(file)
        else:
            NotImplementedError('Other formats than cube not implemented')

        self.compute_3DFT(dk3D, value)
        self.kmap = {}

    def get_kmap(self, E_kin=30, dk=0.03, phi=0, theta=0, psi=0,
                 Ak_type='no', polarization='p', alpha=60, beta=90,
                 gamma=0):
        """Returns a kmap slice from the orbital data.

        Args:
            E_kin (float): Kinetic energy in eV.
            dk (float): Desired k-resolution in kmap in Angstroem^-1.
            phi (float): Euler orientation angle phi in degree.
            theta (float): Euler orientation angle theta in degree.
            psi (float): Euler orientation angle psi in degree.
            Ak_type (string): Treatment of |A.k|^2: either 'no',
                'toroid' or 'NanoESCA'.
            polarization (string): Either 'p', 's', 'C+', 'C-' or
                'CDAD'.   
            alpha (float): Angle of incidence plane in degree.
            beta (float): Azimuth of incidence plane in degree.
            gamma (float): Damping factor for final state in
                Angstroem^-1.
        Returns:
            (PlotData): PlotData containing the kmap slice.
        """

        # Check if E_kin or dk has changed and new hemispherical cut
        # must be computed
        if 'E_kin' in self.kmap:
            if self.kmap['E_kin'] != E_kin or self.kmap['dk'] != dk:
                new_E_kin = True

            else:
                new_E_kin = False
        else:
            new_E_kin = True

        if new_E_kin:
            self.set_kinetic_energy(E_kin, dk)

        # Rotate molecule (that is, rotate hemisphere)
        if phi != 0 or theta != 0 or psi != 0:
            self.set_orientation(phi, theta, psi)

        self.set_polarization(Ak_type, polarization, alpha, beta,
                              gamma)
        
        return PlotData(self.Ak['data']*self.kmap['data'], 
                        self.kmap['krange'])


    def change_polarization(self, Ak_type='no', polarization='p', alpha=60, beta=90,
                                  gamma=0):
        
        self.set_polarization(Ak_type, polarization, alpha, beta,
                              gamma)
        return PlotData(self.Ak['data']*self.kmap['data'], 
                        self.kmap['krange'])


    def compute_3DFT(self, dk3D, value):
        """Compute 3D-FT."""

        # Determine required size (nkx,nky,nkz) of 3D-FT array to reach
        # desired resolution dk3D
        pad_x = max(
            int(2 * np.pi / (dk3D * self.psi['dx'])) - self.psi['nx'], 0)
        pad_y = max(
            int(2 * np.pi / (dk3D * self.psi['dy'])) - self.psi['ny'], 0)
        pad_z = max(
            int(2 * np.pi / (dk3D * self.psi['dz'])) - self.psi['nz'], 0)
        nkx = self.psi['nx'] + pad_x
        nky = self.psi['ny'] + pad_y
        nkz = self.psi['nz'] + pad_z

        # Compute 3D FFT
        psik = np.fft.fftshift(np.fft.fftn(self.psi['data'],
                                           s=[nkx, nky, nkz]))
        if value == 'real':
            psik = np.real(psik)

        elif value == 'imag':
            psik = np.imag(psik)

        elif value == 'abs':
            psik = np.abs(psik)

        else:
            psik = np.abs(psik)**2

        # Set up k-grids for 3D-FT
        kx = self.set_3Dkgrid(nkx, self.psi['dx'])
        ky = self.set_3Dkgrid(nky, self.psi['dy'])
        kz = self.set_3Dkgrid(nkz, self.psi['dz'])

        # Define interpolating function to be used later for kmap
        # computation
        psik_interp = interp.RegularGridInterpolator((kx, ky, kz), psik,
                                                     bounds_error=False,
                                                     fill_value=np.nan)

        # Set attributes
        self.psik = {'kx': kx, 'ky': ky, 'kz': kz,
                     'value': value,
                     'data': psik,
                     'data_interp': psik_interp}

        # Why? Local variables should only live until end of function
        # anyways...
        # Free memory for psik-array
        del psik

    # Make hemi-spherical cut through 3D Fourier transform
    def set_kinetic_energy(self, E_kin, dk):

        kmax = self.E_to_k(E_kin)
        num_k = int(2 * kmax / dk)
        kxi = np.linspace(-kmax, +kmax, num_k)
        kyi = np.linspace(-kmax, +kmax, num_k)
        krange = ((kxi[0], kxi[-1]), (kyi[0], kyi[-1]))
        KX, KY = np.meshgrid(kxi, kyi, indexing='xy')
        '''Throws warning?'''
        KZ = np.sqrt(kmax**2 - KX**2 - KY**2)
        kxkykz = list(map(lambda a, b, c: (a, b, c),
                          KX.flatten(), KY.flatten(), KZ.flatten()))
        data = np.reshape(self.psik['data_interp'](kxkykz), (num_k, num_k))

        # Set kmap attributes
        self.kmap = {'E_kin': E_kin, 'dk': dk, 'krange': krange,
                     'KX': KX, 'KY': KY, 'KZ': KZ,
                     'phi': 0, 'theta': 0, 'psi': 0,
                     'data': data}

    # Rotate hemisphere KX, KY, KZ by Euler angles phi, theta, psi
    def set_orientation(self, phi, theta, psi):

        KX, KY, KZ = self.kmap['KX'], self.kmap['KY'], self.kmap['KZ']
        nkx = KX.shape[0]
        nky = KX.shape[1]
        r = self.compute_Euler_matrix(phi, theta, psi)
        r = r.T

        # KXr, KYr, KZr are the k-coordinates of the rotated hemisphere
        KXr = r[0, 0] * KX + r[0, 1] * KY + r[0, 2] * KZ
        KYr = r[1, 0] * KX + r[1, 1] * KY + r[1, 2] * KZ
        KZr = r[2, 0] * KX + r[2, 1] * KY + r[2, 2] * KZ
        kxkykz = list(map(lambda a, b, c: (a, b, c),
                          KXr.flatten(), KYr.flatten(), KZr.flatten()))
        data = np.reshape(self.psik['data_interp'](kxkykz), (nkx, nky))

        # update attributes
        self.kmap['phi'] = phi
        self.kmap['theta'] = theta
        self.kmap['psi'] = psi
        self.kmap['data'] = data

    def set_polarization(self, Ak_type, polarization, alpha, beta, gamma):

        if Ak_type == 'no':  # Set |A.k|^2 to 1
            self.Ak = {'Ak_type': Ak_type,
                       'polarization': None,
                       'alpha': None,
                       'beta': None,
                       'gamma': None,
                       'data': np.ones_like(self.kmap['data'])}

            return


        # Convert angles to rad and compute sin and cos for later use
        a = np.radians(alpha)
        b = np.radians(beta)
        sin_a = np.sin(a)
        cos_a = np.cos(a)
        sin_b = np.sin(b)
        cos_b = np.cos(b)

        # Compute gamma according to inelastic free mean path
        if gamma == 'auto':
            # lambda is calculated from the "universal curve" empirical
            # relation
            E_kin = self.kmap['E_kin']
            c1 = 143
            c2 = 0.054
            lam = c1 * Ekin**(-2) + c2 * np.sqrt(Ekin)
            lam *= 10
            gamma = 1 / lam

        # Retrieve k-grid from kmap
        kx, ky, kz = self.kmap['KX'], self.kmap['KY'], self.kmap['KZ']

        # At the toroid, the emitted electron is always in the plane of
        # incidence and the sample is rotated
        if Ak_type == 'toroid':
            # Magnitude of k-vector
            k = kx**2 + ky**2 + kz**2
            # Parallel component of k-vector
            kpar = np.sqrt(k - kz**2)
            # |A.k|^2 factor
            Ak = (kpar * cos_a + kz * sin_a)**2

        # At the NanoESCA, either p-polarization ,s-polarization, or
        # circularly polarized light can be simulated
        elif Ak_type == 'NanoESCA':
            # In-plane = p-polarization
            if polarization == 'p':
                Ak = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                Ak = Ak**2 + gamma**2 * sin_a**2

            # Out-of-plane = s-polarization
            elif polarization == 's':
                Ak = -kx * sin_b + ky * cos_b
                Ak = Ak**2

            # Circularly polarized light (right-handed)
            elif polarization == 'C+':
                polp = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                pols = -kx * sin_b + ky * cos_b
                Ak = 0.5 * (polp**2 + gamma**2 * sin_a**2) + 0.5 * \
                    pols**2 - (sin_b * kx - cos_b * ky) * gamma * sin_a

            # Circularly polarized light (left-handed)
            elif polarization == 'C-':
                polp = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                pols = -kx * sin_b + ky * cos_b
                Ak = 0.5 * (polp**2 + gamma**2 * sin_a**2) + 0.5 * \
                    pols**2 + (sin_b * kx - cos_b * ky) * gamma * sin_a

            # CDAD-signal (right-handed - left-handed) using empirically
            # damped plane wave
            elif polarization == 'CDAD':
                # Compare Equation (31) in S. Moser, J. Electr. Spectr.
                # Rel. Phen. 214, 29-52 (2017).
                Ak = -2 * (sin_b * kx - cos_b * ky) * gamma * sin_a

#        # Multiply |A.k|^2 with kmap
#        self.kmap['data'] *= Ak

        # Set attributes
        self.Ak = {'Ak_type': Ak_type,
                   'polarization': polarization,
                   'alpha': alpha,
                   'beta': beta,
                   'gamma': gamma,
                   'data': Ak}

    def _read_cube(self, file):
        """ Read orbital data from cube file."""

        ''' File and path to file are both string. Should _read_cube
        get the file path or the file itself?
        if type(file) == str:
            orbfile = open(file, "r")
            lines   = orbfile.readlines()
            orbfile.close()
        else:
        '''
        # Split the entire file into separate lines
        lines = file.split('\n')

        # Set up real space grid info
        # Conversion factor from Bohr to Angstroem
        b2a = 0.529177105787531

        x0, y0, z0 = b2a * float(lines[2].split()[1]), b2a * float(
            lines[2].split()[2]), b2a * float(lines[2].split()[3])
        nx, ny, nz = int(lines[3].split()[0]), int(
            lines[4].split()[0]), int(lines[5].split()[0])
        dx, dy, dz = b2a * float(lines[3].split()[1]), b2a * float(
            lines[4].split()[2]), b2a * float(lines[5].split()[3])
        lx, ly, lz = (nx - 1) * dx, (ny - 1) * dy, (nz - 1) * dz
        x = np.linspace(x0, x0 + lx, nx)
        y = np.linspace(y0, y0 + ly, ny)
        z = np.linspace(z0, z0 + lz, nz)

        # Read atomic coordinates
        # Number of atoms from line 3
        num_atom = int(lines[2].split()[0])
        chemical_numbers = []
        atomic_coordinates = []
        for line in lines[6:6 + num_atom]:
            words = line.split()
            chemical_numbers.append(int(words[0]))
            a, b, c = float(words[2]), float(words[3]), float(words[4])
            atomic_coordinates.append([b2a * a, b2a * b, b2a * c])

        atomic_coordinates = np.array(atomic_coordinates)

        # Now read cube data
        data = []
        for line in lines[(6 + num_atom):]:
            words = line.split()
            for word in words:
                data.append(float(word))
        # Conversion to 3D-numpy array
        data = np.reshape(np.array(data), (nx, ny, nz))

        # set attributes
        self.psi = {'nx': nx, 'ny': ny, 'nz': nz,
                    'dx': dx, 'dy': dy, 'dz': dz,
                    'x': x, 'y': y, 'z': z,
                    'data': data}
        self.molecule = {'num_atom': num_atom,
                         'chemical_numbers': chemical_numbers,
                         'atomic_coordinates': atomic_coordinates}

    def set_3Dkgrid(self, nk, delta):

        L = (nk - 1) * delta
        dk = 2 * np.pi / L
        if (nk % 2 == 0):
            shiftk = -dk / 2
        else:
            shiftk = 0
        k = shiftk + np.arange(-0.5 * (nk - 1) * dk, 0.5 * nk * dk, dk)

        return k

    def E_to_k(self, E_kin):
        """ Convert kinetic energy in eV to k in Anstroem^-1."""

        # Electron mass
        m = 9.10938356e-31
        # Reduced Planck constant
        hbar = 1.0545718e-34
        # Electron charge
        e = 1.60217662e-19

        fac = 2 * 1e-20 * e * m / hbar**2

        return np.sqrt(fac * E_kin)

    def compute_Euler_matrix(self, phi, theta, psi):
        """Compute rotation matrix according to Eq. (M3.10.3) of
        Lang-Pucker"""

        # Compute sines and cosines of angles
        sin_phi = np.sin(np.radians(phi))
        cos_phi = np.cos(np.radians(phi))
        sin_theta = np.sin(np.radians(theta))
        cos_theta = np.cos(np.radians(theta))
        sin_psi = np.sin(np.radians(psi))
        cos_psi = np.cos(np.radians(psi))

        # Euler matrix r according to eq. (M3.10.3) of Lang-Pucker
        r = np.zeros((3, 3))
        r[0, 0] = cos_phi * cos_psi - sin_phi * cos_theta * sin_psi
        r[1, 0] = -cos_phi * sin_psi - sin_phi * cos_theta * cos_psi
        r[2, 0] = sin_phi * sin_theta

        r[0, 1] = sin_phi * cos_psi + cos_phi * cos_theta * sin_psi
        r[1, 1] = -sin_phi * sin_psi + cos_phi * cos_theta * cos_psi
        r[2, 1] = -cos_phi * sin_theta

        r[0, 2] = sin_theta * sin_psi
        r[1, 2] = sin_theta * cos_psi
        r[2, 2] = cos_theta

        return r
