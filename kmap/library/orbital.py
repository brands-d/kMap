"""Defines the Orbital class.

This file defines a class named Orbital designed to read, hold,
calculate and slice data from cube files.
"""

import numpy as np
import scipy.interpolate as interp
from kmap.library.plotdata import PlotData
from kmap.library.misc import energy_to_k, compute_Euler_matrix

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
        E_kin_max (float): maximum kinetic energy in eV is used to
            reduce the size of the 3D-numpy-array in momentum space
        value (string): choose between 'real', 'imag', 'abs' or 'abs2'
            for Re(), Im(), |..| or |..|^2

    Attributes:

    """

    def __init__(self, file, file_format='cube', dk3D=0.15, E_kin_max=150,
                 value='abs2'):
        # Read orbital data from file
        if file_format == 'cube':
            self._read_cube(file)
        else:
            NotImplementedError('Other formats than cube not implemented')

        self.compute_3DFT(dk3D, E_kin_max, value)
        self.kmap = {}
        self.Ak = {}

    def get_kmap(self, E_kin=30, dk=0.03, phi=0, theta=0, psi=0,
                 Ak_type='no', polarization='p', alpha=60, beta=90,
                 gamma=0, symmetrization='no', s_share=0.694):
        """Returns a kmap slice from the orbital data.

        Args:
            E_kin (float): Kinetic energy in eV.
            dk (float): Desired k-resolution in kmap in Angstroem^-1.
            phi (float): Euler orientation angle phi in degree.
            theta (float): Euler orientation angle theta in degree.
            psi (float): Euler orientation angle psi in degree.
            Ak_type (string): Treatment of |A.k|^2: either 'no',
                'toroid', 'NanoESCA', 'only-toroid' or 'only-NanoESCA'.
            polarization (string): Either 'p', 's', 'unpolarized', 
                'C+', 'C-' or 'CDAD'.   
            alpha (float): Angle of incidence plane in degree.
            beta (float): Azimuth of incidence plane in degree.
            gamma (float/str): Damping factor for final state in
                Angstroem^-1. str = 'auto' sets gamms automatically
            symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
            s_share (float): share of s-polarized light for the case
                of unpolarized light (should be between 0 and 1)

        Returns:
            (PlotData): PlotData containing the kmap slice.
        """

        # Compute new hemispherical cut if E_kin or dk has changed
        new_cut = self.check_new_cut(E_kin, dk)
        if new_cut: self.set_kinetic_energy(E_kin, dk)

        # Rotate molecule (that is, rotate hemisphere) if angles have changed
        # ... and symmetrize kmap if necessary
        new_orientation = self.check_new_orientation(phi, theta, psi)
        new_symmetrization = self.check_new_symmetrization(symmetrization)
        if new_symmetrization or new_orientation:
            self.set_orientation(phi, theta, psi)
            self.set_symmetry(symmetrization)

        # Compute polarization factor if parameters have changed
        new_Ak = self.check_new_Ak(Ak_type, polarization, alpha, beta, gamma,
                                   s_share)
        if new_cut or new_Ak: self.set_polarization(Ak_type, polarization,
                                                    alpha, beta, gamma,
                                                    s_share)

        if Ak_type == 'only-toroid' or Ak_type == 'only-NanoESCA':
            return PlotData(self.Ak['data'], self.kmap['krange'])

        else:
            return PlotData(self.Ak['data'] * self.kmap['data'],
                            self.kmap['krange'])

    def change_polarization(self, Ak_type='no', polarization='p', alpha=60,
                            beta=90,
                            gamma=0, s_share=0.694):
        self.set_polarization(Ak_type, polarization, alpha, beta,
                              gamma, s_share)
        return PlotData(self.Ak['data'] * self.kmap['data'],
                        self.kmap['krange'])

    def compute_3DFT(self, dk3D, E_kin_max, value):
        """Compute 3D-FT."""

        # Determine required size (nkx,nky,nkz) of 3D-FT array to reach
        # desired resolution dk3D
        pad_x = max(
            int(2 * np.pi / (dk3D * self.psi['dx'])) - self.psi['nx'], 0)
        pad_y = max(
            int(2 * np.pi / (dk3D * self.psi['dy'])) - self.psi['ny'], 0)
        pad_z = max(
            int(2 * np.pi / (dk3D * self.psi['dz'])) - self.psi['nz'], 0)

        if pad_x % 2 == 1: pad_x += 1  # make sure it's an even number
        if pad_y % 2 == 1: pad_y += 1  # make sure it's an even number
        if pad_z % 2 == 1: pad_z += 1  # make sure it's an even number

        nkx = self.psi['nx'] + pad_x
        nky = self.psi['ny'] + pad_y
        nkz = self.psi['nz'] + pad_z

        # Set up k-grids for 3D-FT
        kx = self.set_3Dkgrid(nkx, self.psi['dx'])
        ky = self.set_3Dkgrid(nky, self.psi['dy'])
        kz = self.set_3Dkgrid(nkz, self.psi['dz'])

        # Compute 3D FFT
        # !! TESTING !!! This is supposed to yield also proper Real- and Imaginary parts!!
        #        print(nkx, nky, nkz)
        #        print(pad_x, pad_y, pad_z)
        psi_padded = np.pad(self.psi['data'],
                            pad_width=(
                                (pad_x // 2, pad_x // 2),
                                (pad_y // 2, pad_y // 2),
                                (pad_z // 2, pad_z // 2)),
                            mode='constant',
                            constant_values=(0, 0))
        psi_padded = np.fft.ifftshift(psi_padded)
        psik = np.fft.fftshift(np.fft.fftn(psi_padded))

        # THIS IS THE OLD AND WELL TESTED WAY TO Compute 3D FFT
        #        psik = np.fft.fftshift(np.fft.fftn(self.psi['data'],
        #                                           s=[nkx, nky, nkz]))

        # properly normalize wave function in momentum space
        dkx, dky, dkz = kx[1] - kx[0], ky[1] - ky[0], kz[1] - kz[0]
        factor = dkx * dky * dkz * np.sum(np.abs(psik)**2)
        psik /= np.sqrt(factor)

        # Reduce size of array to value given by E_kin_max to save memory
        k_max = energy_to_k(E_kin_max)
        kx_indices = np.where((kx <= k_max) & (kx >= -k_max))[0]
        ky_indices = np.where((ky <= k_max) & (ky >= -k_max))[0]
        kz_indices = np.where((kz <= k_max) & (kz >= -k_max))[0]
        kx = kx[kx_indices]
        ky = ky[ky_indices]
        kz = kz[kz_indices]
        psik = np.take(psik, kx_indices, axis=0)
        psik = np.take(psik, ky_indices, axis=1)
        psik = np.take(psik, kz_indices, axis=2)

        # decide whether real, imaginry part, absolute value, or squared absolute value is used
        if value == 'real':
            psik = np.asarray(np.real(psik), order='C')

        elif value == 'imag':
            psik = np.asarray(np.imag(psik), order='C')

        elif value == 'abs':
            psik = np.abs(psik)

        elif value == 'complex':
            psik = psik

        else:
            psik = np.abs(psik)**2

        # Define interpolating function to be used later for kmap
        # computation
        psik_interp = interp.RegularGridInterpolator((kx, ky, kz), psik,
                                                     bounds_error=False,
                                                     fill_value=np.nan)

        # Set attributes
        self.psik = {'kx': kx, 'ky': ky, 'kz': kz,
                     'E_kin_max': E_kin_max,
                     'value': value,
                     'data': psik,
                     'data_interp': psik_interp}

        # Why? Local variables should only live until end of function
        # anyways...
        # Free memory for psik-array
        del psik

    # Make hemi-spherical cut through 3D Fourier transform
    def set_kinetic_energy(self, E_kin, dk):
        kmax = energy_to_k(E_kin)
        if type(dk) == tuple:
            kxi = dk[0]
            kyi = dk[1]
            num_kx = len(kxi)
            num_ky = len(kyi)
        else:
            num_kx = int(2 * kmax / dk)
            num_ky = int(2 * kmax / dk)
            kxi = np.linspace(-kmax, +kmax, num_kx)
            kyi = np.linspace(-kmax, +kmax, num_ky)

        krange = ((kxi[0], kxi[-1]), (kyi[0], kyi[-1]))
        KX, KY = np.meshgrid(kxi, kyi, indexing='xy')
        KZ = np.sqrt(kmax**2 - KX**2 - KY**2)
        kxkykz = list(map(lambda a, b, c: (a, b, c),
                          KX.flatten(), KY.flatten(), KZ.flatten()))
        data = np.reshape(self.psik['data_interp'](kxkykz), (num_kx, num_ky))

        # Set kmap attributes
        self.kmap = {'E_kin': E_kin, 'dk': dk, 'krange': krange,
                     'KX': KX, 'KY': KY, 'KZ': KZ,
                     'phi': 0, 'theta': 0, 'psi': 0,
                     'data': data}

    def check_new_cut(self, E_kin, dk):
        eps = 1e-10

        new_cut = False

        if 'E_kin' in self.kmap:
            if type(dk) != tuple and type(self.kmap['dk']) != tuple:
                if (np.abs(self.kmap['E_kin'] - E_kin) > eps or
                        np.abs(self.kmap['dk'] - dk) > eps):
                    new_cut = True

            elif type(dk) == tuple and type(self.kmap['dk']) != tuple:
                new_cut = True

            elif type(dk) != tuple and type(self.kmap['dk']) == tuple:
                new_cut = True

            elif type(dk) == tuple and type(self.kmap['dk']) == tuple:
                if np.abs(self.kmap['E_kin'] - E_kin) > eps:
                    new_cut = True

                if dk[0].shape != self.kmap['dk'][0].shape:
                    new_cut = True
                else:
                    if np.any(np.abs(self.kmap['dk'][0] - dk[0]) > eps):
                        new_cut = True

                if dk[1].shape != self.kmap['dk'][1].shape:
                    new_cut = True
                else:
                    if np.any(np.abs(self.kmap['dk'][1] - dk[1]) > eps):
                        new_cut = True

        else:
            new_cut = True

        return new_cut

    # get the (kx,ky) values of the kmap as a list of tuples
    def get_kxkygrid(self):
        KX, KY = self.kmap['KX'], self.kmap['KY']
        return list(map(lambda a, b: (a, b), KX.flatten(), KY.flatten()))

        # Rotate hemisphere KX, KY, KZ by Euler angles phi, theta, psi

    def set_orientation(self, phi, theta, psi):
        KX, KY, KZ = self.kmap['KX'], self.kmap['KY'], self.kmap['KZ']
        nkx = KX.shape[0]
        nky = KX.shape[1]
        r = compute_Euler_matrix(phi, theta, psi)
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

    def check_new_orientation(self, phi, theta, psi):
        eps = 1e-10
        if 'phi' in self.kmap:
            if (np.abs(self.kmap['phi'] - phi) > eps or
                    np.abs(self.kmap['theta'] - theta) > eps or
                    np.abs(self.kmap['psi'] - psi) > eps):
                new_orientation = True

            else:
                new_orientation = False
        else:
            new_orientation = True

        return new_orientation

    def set_polarization(self, Ak_type, polarization, alpha, beta, gamma,
                         s_share):
        if Ak_type == 'no':  # Set |A.k|^2 to 1
            self.Ak = {'Ak_type': Ak_type,
                       'polarization': polarization,
                       'alpha': alpha,
                       'beta': beta,
                       'gamma': gamma,
                       's_share': s_share,
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
            lam = c1 * E_kin**(-2) + c2 * np.sqrt(E_kin)
            lam *= 10
            gamma_calc = 1 / lam
        else:
            gamma_calc = gamma

        # Retrieve k-grid from kmap
        kx, ky, kz = self.kmap['KX'], self.kmap['KY'], self.kmap['KZ']
        # Magnitude of k-vector
        k2 = kx**2 + ky**2 + kz**2
        kmax = energy_to_k(self.kmap['E_kin'])

        # At the toroid, the emitted electron is always in the plane of
        # incidence and the sample is rotated
        if Ak_type == 'toroid' or Ak_type == 'only-toroid':
            # Parallel component of k-vector
            kpar = np.sqrt(k2 - kz**2)
            # |A.k|^2 factor
            Ak = (kpar * cos_a + kz * sin_a)**2

        # At the NanoESCA, either p-polarization ,s-polarization, or
        # circularly polarized light can be simulated
        elif Ak_type == 'NanoESCA' or Ak_type == 'only-NanoESCA':
            # In-plane = p-polarization
            if polarization == 'p':
                Ak = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                Ak = Ak**2 + gamma_calc**2 * sin_a**2

            # Out-of-plane = s-polarization
            elif polarization == 's':
                Ak = -kx * sin_b + ky * cos_b
                Ak = Ak**2
                Ak[kx**2 + ky**2 > kmax**2] = np.nan


            # unpolarized light, e.g. He-lamp 
            # Compare Equation (37) in S. Moser, J. Electr. Spectr.
            # Rel. Phen. 214, 29-52 (2017).  
            # Eq. (37) turned out to be wrong!!!          
            #            elif polarization == 'unpolarized':
            #                Ak = (k2 + gamma_calc**2 + 2*kx*kz*cos_b + 2*ky*kz*sin_b)*np.sin(2*a)
            #                Ak+= (kx**2*sin_b + ky**2*cos_b - kz**2 - gamma_calc**2)*np.cos(2*a)
            #                Ak*= (2/3)

            # unpolarized-light is now correctly treated as average of
            # s- and p-polarized light
            elif polarization == 'unpolarized':
                Ak_p = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                Ak_p = Ak_p**2 + gamma_calc**2 * sin_a**2
                Ak_s = -kx * sin_b + ky * cos_b
                Ak_s = Ak_s**2

                Ak = s_share * Ak_s + (1 - s_share) * Ak_p
                Ak[kx**2 + ky**2 > kmax**2] = np.nan


            # Circularly polarized light (right-handed)
            elif polarization == 'C+':
                polp = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                pols = -kx * sin_b + ky * cos_b
                Ak = 0.5 * (polp**2 + gamma_calc**2 * sin_a**2) + 0.5 * \
                     pols**2 + (sin_b * kx - cos_b * ky) * gamma_calc * sin_a

            # Circularly polarized light (left-handed)
            elif polarization == 'C-':
                polp = kx * cos_a * cos_b + ky * cos_a * sin_b + kz * sin_a
                pols = -kx * sin_b + ky * cos_b
                Ak = 0.5 * (polp**2 + gamma_calc**2 * sin_a**2) + 0.5 * \
                     pols**2 - (sin_b * kx - cos_b * ky) * gamma_calc * sin_a

            # CDAD-signal (right-handed - left-handed) using empirically
            # damped plane wave
            elif polarization == 'CDAD':
                # Compare Equation (31) in S. Moser, J. Electr. Spectr.
                # Rel. Phen. 214, 29-52 (2017).
                Ak = +2 * (sin_b * kx - cos_b * ky) * gamma_calc * sin_a
                Ak[kx**2 + ky**2 > kmax**2] = np.nan

        # Set attributes
        self.Ak = {'Ak_type': Ak_type,
                   'polarization': polarization,
                   'alpha': alpha,
                   'beta': beta,
                   'gamma': gamma,
                   's_share': s_share,
                   'data': Ak}

    def check_new_Ak(self, Ak_type, polarization, alpha, beta, gamma, s_share):
        if 'Ak_type' in self.Ak:
            if (self.Ak['Ak_type'] != Ak_type or
                    self.Ak['polarization'] != polarization or
                    self.Ak['alpha'] != alpha or
                    self.Ak['beta'] != beta or
                    self.Ak['gamma'] != gamma or
                    self.Ak['s_share'] != s_share):
                new_Ak = True

            else:
                new_Ak = False
        else:
            new_Ak = True

        return new_Ak

    def set_symmetry(self, symmetrization):
        """Symmterizes the kmap.

        Args:
            symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'

        """
        data = PlotData(self.kmap['data'], self.kmap['krange'])

        if symmetrization == '2-fold':
            data.symmetrise(symmetry='2-fold', update=True)

        elif symmetrization == '2-fold+mirror':
            data.symmetrise(symmetry='2-fold', mirror=True,
                                         update=True)

        elif symmetrization == '3-fold':
            data.symmetrise(symmetry='3-fold', update=True)

        elif symmetrization == '3-fold+mirror':
            data.symmetrise(symmetry='3-fold', mirror=True,
                                         update=True)

        elif symmetrization == '4-fold':
            data.symmetrise(symmetry='4-fold', update=True)

        elif symmetrization == '4-fold+mirror':
            data.symmetrise(symmetry='4-fold', mirror=True,
                                         update=True)

        self.kmap['data'] = data.data
        self.kmap['symmetrization'] = symmetrization

    def check_new_symmetrization(self, symmetrization):
        if 'symmetrization' in self.kmap:
            if self.kmap['symmetrization'] != symmetrization:
                new_symmetrization = True

            else:
                new_symmetrization = False
        else:
            new_symmetrization = True

        return new_symmetrization

    def plot(self, ax, title=None, kxlim=None, kylim=None, interpolation='bicubic',
                       value='leave_as_is'):

        """Creates a plot of the kmap in axes-obeject ax.

        Args:
            

        """

        # prepare data
        data   = self.Ak['data']*self.kmap['data'] 
        if value ==  'abs':
            data = np.abs(data)

        elif value == 'real':
            data = np.asarray(np.real(data), order='C')

        elif value == 'imag':
            data = np.asarray(np.imag(data), order='C')


        krange = self.kmap['krange']
        limits = [krange[0][0], krange[0][1], krange[1][0], krange[1][1]]

        # plot kmap       
        im = ax.imshow(data,
                       extent=limits,
                       interpolation=interpolation,
                       origin='lower',
                       cmap='jet')

        # format plot
        ax.set_aspect('equal')
        #        ax.set_xlabel(r'$\kappa_x(1/\AA)$')
        #        ax.set_ylabel(r'$\kappa_y(1/\AA)$')
        ax.set_xlabel(r'$k_x$ (Å$^{-1}$)')
        ax.set_ylabel(r'$k_y$ (Å$^{-1}$)')

        if kxlim != None:
            ax.set_xlim(kxlim[0], kxlim[1])
        if kylim != None:
            ax.set_ylim(kxlim[0], kxlim[1])

        if title != None:
            ax.set_title(title)

        return

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

        name = lines[1].strip()

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
        self.psi = {'name': name,
                    'nx': nx, 'ny': ny, 'nz': nz,
                    'dx': dx, 'dy': dy, 'dz': dz,
                    'x': x, 'y': y, 'z': z,
                    'data': data}
        self.molecule = {'num_atom': num_atom,
                         'chemical_numbers': chemical_numbers,
                         'atomic_coordinates': atomic_coordinates}

    def get_bonds(self, lower_factor=0.7, upper_factor=1.2):
        """ returns a list of bond used for plotting the molecular structure.

        Args:
            lower_factor (float): lower bound for drawing bonds w.r.t sum of covalent radii
            upper_factor (float): upper bound for drawing bonds w.r.t sum of covalent radii
        """
        covalent_R = {1: 0.32, 2: 0.32,  # H, He
                      3: 1.34, 4: 0.90, 5: 0.82, 6: 0.77, 7: 0.71, 8: 0.73,
                      9: 0.71, 10: 0.69,  # Li - Ne
                      11: 1.54, 12: 1.30, 13: 1.18, 14: 1.11, 15: 1.06,
                      16: 1.02, 17: 0.99, 18: 0.97,  # Na- Ar
                      19: 1.96, 20: 1.74, 21: 1.44, 22: 1.36, 23: 1.25,
                      24: 1.27, 25: 1.39, 26: 1.25,  # K - Fe
                      27: 1.26, 28: 1.21, 29: 1.38, 30: 1.31, 31: 1.26,
                      32: 1.22, 33: 1.21, 34: 1.16,  # Co- Se
                      35: 1.14, 36: 1.10,  # Br, Kr
                      37: 2.11, 38: 1.92, 39: 1.62, 40: 1.48, 41: 1.37,
                      41: 1.45, 43: 1.31, 44: 1.26,  # Rb -Ru
                      45: 1.35, 46: 1.31, 47: 1.53, 48: 1.48, 49: 1.44,
                      50: 1.41, 51: 1.38, 52: 1.35,  # Rh -Te
                      53: 1.33, 54: 1.30,  # I, Xe
                      55: 2.25, 56: 1.98, 57: 1.69, 72: 1.50, 73: 1.38,
                      74: 1.46, 75: 1.59, 76: 1.28,  # Cs -Os
                      77: 1.37, 78: 1.38, 79: 1.38, 80: 1.49, 81: 1.48,
                      82: 1.46, 83: 1.46, 84: 1.40,  # Ir -Po
                      85: 1.45, 86: 1.45}  # At, Rn

        dx, dy, dz = self.psi['dx'], self.psi['dy'], self.psi['dz']
        coordinates = self.molecule['atomic_coordinates']
        Z_list = self.molecule['chemical_numbers']
        bonds = []
        for atom1, Z1 in zip(coordinates, Z_list):
            x1, y1, z1 = atom1[0], atom1[1], atom1[2]
            R1 = covalent_R[Z1]
            for atom2, Z2 in zip(coordinates, Z_list):
                x2, y2, z2 = atom2[0], atom2[1], atom2[2]
                R2 = covalent_R[Z2]
                R = R1 + R2  # sum of covalent radii
                distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
                if lower_factor * R <= distance <= upper_factor * R:
                    bond = [[x1 / dx, y1 / dy, z1 / dz],
                            [x2 / dx, y2 / dy, z2 / dz]]
                    bonds.append(np.array(bond))

        return bonds

    def set_3Dkgrid(self, nk, delta):
        k_min = -np.pi / delta
        k_max = +np.pi / delta
        k, dk = np.linspace(k_min, k_max, nk, retstep=True)
        if nk % 2 == 0:
            k = k - dk / 2

        return k
