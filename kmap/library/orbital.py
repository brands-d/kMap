"""Defines the Orbital class.

This file defines a class named Orbital designed to read, hold,
calculate and slice data from cube files.
"""

import numpy as np
import scipy.interpolate as interp
from scipy.ndimage import rotate
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
        E_kin_max (float): maximum kinetic energy in eV is used to
            reduce the size of the 3D-numpy-array in momentum space
        value (string): choose between 'real', 'imag', 'abs' or 'abs2'
            for Re(), Im(), |..| or |..|^2

    Attributes:

    """

    def __init__(self, file, file_format='cube', dk3D=0.15, E_kin_max=150,value='abs2'):
        
        # Read orbital data from file
        if file_format == 'cube': 
            self._read_cube(file)
        else:
            NotImplementedError('Other formats than cube not implemented')

        self.compute_3DFT(dk3D, E_kin_max, value)
        self.kmap = {}
        self.Ak   = {}

    def get_kmap(self, E_kin=30, dk=0.03, phi=0, theta=0, psi=0,
                 Ak_type='no', polarization='p', alpha=60, beta=90,
                 gamma=0,symmetrization='no'):
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
            gamma (float/str): Damping factor for final state in
                Angstroem^-1. str = 'auto' sets gamms automatically
            symmetrization (str): either 'no', '2-fold', '2-fold+mirror',
                '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'
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
        new_Ak  = self.check_new_Ak(Ak_type, polarization, alpha, beta, gamma)
        if new_cut or new_Ak: self.set_polarization(Ak_type, polarization, 
                                         alpha, beta,gamma)

        return PlotData(self.Ak['data']*self.kmap['data'], 
                        self.kmap['krange'])


    def change_polarization(self, Ak_type='no', polarization='p', alpha=60, beta=90,
                                  gamma=0):
        
        self.set_polarization(Ak_type, polarization, alpha, beta,
                              gamma)
        return PlotData(self.Ak['data']*self.kmap['data'], 
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

        if pad_x%2 == 1: pad_x += 1  # make sure it's an even number
        if pad_y%2 == 1: pad_y += 1  # make sure it's an even number
        if pad_z%2 == 1: pad_z += 1  # make sure it's an even number

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
                      pad_width=((pad_x//2,pad_x//2), (pad_y//2,pad_y//2), (pad_z//2,pad_z//2)),
                      mode='constant',
                      constant_values=(0,0))
        psi_padded = np.fft.ifftshift(psi_padded)                                
        psik = np.fft.fftshift(np.fft.fftn(psi_padded))

       # THIS IS THE OLD AND WELL TESTED WAY TO Compute 3D FFT
#        psik = np.fft.fftshift(np.fft.fftn(self.psi['data'],
#                                           s=[nkx, nky, nkz]))

        # properly normalize wave function in momentum space
        dkx, dky, dkz = kx[1]-kx[0], ky[1]-ky[0], kz[1]-kz[0]
        factor        = dkx*dky*dkz*np.sum(np.abs(psik)**2)
        psik         /= np.sqrt(factor)

        # Reduce size of array to value given by E_kin_max to save memory
        k_max      = self.E_to_k(E_kin_max)
        kx_indices = np.where((kx <= k_max) & (kx >= -k_max))[0]
        ky_indices = np.where((ky <= k_max) & (ky >= -k_max))[0]
        kz_indices = np.where((kz <= k_max) & (kz >= -k_max))[0]    
        kx         = kx[kx_indices]
        ky         = ky[ky_indices]
        kz         = kz[kz_indices]
        psik       = np.take(psik, kx_indices, axis=0)
        psik       = np.take(psik, ky_indices, axis=1)
        psik       = np.take(psik, kz_indices, axis=2)

        # decide whether real, imaginry part, absolute value, or squared absolute value is used
        if value == 'real':
            psik = np.asarray(np.real(psik), order='C')

        elif value == 'imag':
            psik = np.asarray(np.imag(psik), order='C')

        elif value == 'abs':
            psik = np.abs(psik)

        else:
            psik = np.abs(psik)**2


        # Define interpolating function to be used later for kmap
        # computation
        psik_interp = interp.RegularGridInterpolator((kx, ky, kz), psik,
                                                     bounds_error=False,
                                                     fill_value=np.nan)

        # Set attributes
        self.psik = {'kx': kx, 'ky': ky, 'kz': kz,
                     'E_kin_max':E_kin_max,
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
        KZ = np.sqrt(kmax**2 - KX**2 - KY**2)
        kxkykz = list(map(lambda a, b, c: (a, b, c),
                          KX.flatten(), KY.flatten(), KZ.flatten()))
        data = np.reshape(self.psik['data_interp'](kxkykz), (num_k, num_k))

        # Set kmap attributes
        self.kmap = {'E_kin': E_kin, 'dk': dk, 'krange': krange,
                     'KX': KX, 'KY': KY, 'KZ': KZ,
                     'phi': 0, 'theta': 0, 'psi': 0,
                     'data': data}

    def check_new_cut(self, E_kin, dk):

        eps = 1e-10
        if 'E_kin' in self.kmap:
            if (np.abs(self.kmap['E_kin'] - E_kin) > eps or 
                np.abs(self.kmap['dk']    - dk)    > eps):
                  new_cut = True

            else:
                  new_cut = False
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

    def check_new_orientation(self, phi, theta, psi):

        eps = 1e-10
        if 'phi' in self.kmap:
            if (np.abs(self.kmap['phi']   - phi)   > eps or 
                np.abs(self.kmap['theta'] - theta) > eps or
                np.abs(self.kmap['psi']   - psi)   > eps ):
                  new_orientation = True

            else:
                  new_orientation = False
        else:
            new_orientation = True

        return new_orientation


    def set_polarization(self, Ak_type, polarization, alpha, beta, gamma):

        if Ak_type == 'no':  # Set |A.k|^2 to 1
            self.Ak = {'Ak_type': Ak_type,
                       'polarization': polarization,
                       'alpha': alpha,
                       'beta': beta,
                       'gamma': gamma,
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
                Ak = Ak**2 + gamma_calc**2 * sin_a**2

            # Out-of-plane = s-polarization
            elif polarization == 's':
                Ak = -kx * sin_b + ky * cos_b
                Ak = Ak**2

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


        # Set attributes
        self.Ak = {'Ak_type': Ak_type,
                   'polarization': polarization,
                   'alpha': alpha,
                   'beta': beta,
                   'gamma': gamma,
                   'data': Ak}

    def check_new_Ak(self, Ak_type, polarization, alpha, beta, gamma):

        if 'Ak_type' in self.Ak:

            if (self.Ak['Ak_type']      != Ak_type      or
                self.Ak['polarization'] != polarization or
                self.Ak['alpha']        != alpha        or
                self.Ak['beta']         != beta         or
                self.Ak['gamma']        != gamma):
 
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
        if symmetrization == 'no':
            self.kmap['symmetrization'] = 'no'
            return 

        data = self.kmap['data']

        if symmetrization == '2-fold': 
            data += rotate(np.nan_to_num(data), 180, reshape=False)
            data /= 2
                    
        elif symmetrization == '2-fold+mirror': 
            data += rotate(np.nan_to_num(data), 180, reshape=False)
            data += np.flip(data, 0)  # mirror map with respect to first axis
            data /= 4

        elif symmetrization == '3-fold': 
            data1 = rotate(np.nan_to_num(data), 120, reshape=False)
            data2 = rotate(np.nan_to_num(data), 240, reshape=False)
            data += (data1 + data2)
            data /= 3
                     
        elif symmetrization == '3-fold+mirror': 
            data1 = rotate(np.nan_to_num(data), 120, reshape=False)
            data2 = rotate(np.nan_to_num(data), 240, reshape=False)
            data += (data1 + data2)
            data += np.flip(data, 0)
            data /= 6

        elif symmetrization == '4-fold': 
            data1 = rotate(np.nan_to_num(data), 90, reshape=False)
            data2 = rotate(np.nan_to_num(data), 180, reshape=False)
            data3 = rotate(np.nan_to_num(data), 270, reshape=False)
            data += (data1 + data2 + data3)
            data /= 4
                      
        elif symmetrization == '4-fold+mirror': 
            data1 = rotate(np.nan_to_num(data), 90, reshape=False)
            data2 = rotate(np.nan_to_num(data), 180, reshape=False)
            data3 = rotate(np.nan_to_num(data), 270, reshape=False)
            data += (data1 + data2 + data3)
            data += np.flip(data, 0)  # mirror map with respect to first axis
            data += np.flip(data, 1)  # mirror map with respect to second axis
            data /= 8

        self.kmap['symmetrization'] = symmetrization
        self.kmap['data'] = data
        return

    def check_new_symmetrization(self, symmetrization):

        if 'symmetrization' in self.kmap:

            if self.kmap['symmetrization'] != symmetrization:
 
                  new_symmetrization = True

            else:
                  new_symmetrization = False
        else:
            new_symmetrization = True

        return new_symmetrization


    def plot(self, ax, title=None, kxlim=None, kylim=None):
        """Creates a plot of the kmap in axes-obeject ax.

        Args:
            

        """

        # prepare data
        data   = self.Ak['data']*self.kmap['data']  
        krange = self.kmap['krange']
        limits = [krange[0][0], krange[0][1], krange[1][0], krange[1][1]]

        # plot kmap       
        im = ax.imshow(data,
                      extent=limits,
                      interpolation='bicubic',
                      origin='lower',
                      cmap='jet')

        # format plot
        ax.set_aspect('equal')
        ax.set_xlabel(r'$\kappa_x(1/\AA)$')
        ax.set_ylabel(r'$\kappa_y(1/\AA)$')

        if kxlim != None:
            ax.set_xlim(kxlim[0],kxlim[1])        
        if kylim != None:
            ax.set_ylim(kxlim[0],kxlim[1])        

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

    def get_bonds(self,min_bond_length=0.8,max_bond_length=1.8):
        """ returns a list of bond used for plotting the molecular structure.

        Args:
            min_bond_length (float): minimum distance between atoms 
                                     for drawing bonds
            max_bond_length (float): maximum distance between atoms 
                                     for drawing bonds
        """
        
        dx,dy,dz    = self.psi['dx'], self.psi['dy'], self.psi['dz'] 
        coordinates = self.molecule['atomic_coordinates']
        bonds       = []
        for atom1 in coordinates:
            x1,y1,z1 = atom1[0], atom1[1], atom1[2]
            for atom2 in coordinates:
                x2,y2,z2 = atom2[0], atom2[1], atom2[2]    
                distance = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                if min_bond_length <= distance <= max_bond_length:
                    bond = [[x1/dx,y1/dy,z1/dz], [x2/dx,y2/dy,z2/dz]] 
                    bonds.append(np.array(bond))

        return bonds

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
