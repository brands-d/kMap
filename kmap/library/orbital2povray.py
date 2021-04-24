# Third Party Imports
import numpy as np
import pyqtgraph as pg
from configparser import ConfigParser


number2symbol = {1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',
                11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',19:'K',20:'Ca',
                21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',27:'Co',28:'Ni',29:'Cu',30:'Zn',
                31:'Ga',32:'Ge',33:'As',34:'Se',35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',
                41:'Nb',42:'Mo',43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',
                51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba',57:'La',58:'Ce',59:'Pr',60:'Nd',
                61:'Pm',62:'Sm',63:'Eu',64:'Gd',65:'Tb',66:'Dy',67:'Ho',68:'Er',69:'Tm',70:'Yb',
                71:'Lu',72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',79:'Au',80:'Hg',
                81:'Tl',82:'Pb',83:'Bi',84:'Po',85:'At',86:'Rn',87:'Fr',88:'Ra',89:'Ac',90:'Th',
                91:'Pa',92:'U',93:'Np',94:'Pu',95:'Am',96:'Cm',97:'Bk',98:'Cf',99:'Es',100:'Fm'}


class Orbital2Povray():
    """
    This file defines a class named Orbital2Povray designed to convert
    3D orbital-data from the Orbital class into povray format for rendering
    the molecular backbone as well as isosurface of the 3D data 
    either in real space or in reciprocal space

    Args:
        orbital (Orbital): instance of the Orbital class from kmap.library.orbital
        domain (string): choose between 'real' or 'reciprocal'
        isovals (list): list of floats with iso-surface valiues as fraction of maximum value of data cube

    Public Methods:
        get_bonds(lower_factor=0.8, upper_factor=1.2):
        get_isosurface(isoval):
        get_isocolor(index):
        write_povfile(filename):
        run_povray(executable)

    Private Methods:
        _write_atoms(self, file):
        _write_bonds(self, file):
        _write_isosurface(self, file, isovalue, vertices, faces, color):
        _get_atomsetting(self, element):
        _write_header(self, file):
        _write_macros(self, file):

    Attributes:
        domain (str): either 'real' or 'reciprocal' for real or momentum space isosurface
        data (3D numpy-array): 3D data cube used to compute isosurface
        grid (dict): keys, nx, ny, nz, dx, dy, dz specifying data grid
        molecule (dict): contains chemical elements and atomic positions of molecule
        bonds (list): list of atom indices for bond connectivity
        settings (ConfigParser): settings used in povray input file
        isovalues (list): list of floats specifying the values for the isosurface(s)
        pov_file (str): filename of povray file

    """
    def __init__(self, orbital, 
                       domain='real',
                       settings='settings_povray.ini'):

        if domain == 'real':
            self.domain = 'real'
            self.data = orbital.psi['data']
            self.grid = {'nx':orbital.psi['nx'], 
                         'ny':orbital.psi['ny'],
                         'nz':orbital.psi['nz'],
                         'dx':orbital.psi['dx'],
                         'dy':orbital.psi['dy'],
                         'dz':orbital.psi['dz']}
            self.molecule = orbital.molecule
            self.bonds = self.get_bonds()

        elif domain == 'reciprocal':
            self.domain = 'reciprocal'
            self.data = orbital.psik['data']
            self.grid = {'nx':orbital.psik['data'].shape[0], 
                         'ny':orbital.psik['data'].shape[1],
                         'nz':orbital.psik['data'].shape[2],
                         'dx':orbital.psik['kx'][1] - orbital.psik['kx'][0],
                         'dy':orbital.psik['ky'][1] - orbital.psik['ky'][0],
                         'dz':orbital.psik['kz'][1] - orbital.psik['kz'][0]}

        self.settings = ConfigParser()
        self.settings.read(settings)
        
        self.isovalues = self.settings['isosurface']['isovalues']

    def get_bonds(self, lower_factor=0.8, upper_factor=1.2):
        """ returns a list of bonds as list of atom indices

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

        coordinates = self.molecule['atomic_coordinates']
        Z_list = self.molecule['chemical_numbers']
        bonds = []
        for i in range(len(Z_list)):
            x1, y1, z1 = coordinates[i][0], coordinates[i][1], coordinates[i][2]
            R1 = covalent_R[Z_list[i]]
            for j in range(i+1, len(Z_list)):
                x2, y2, z2 = coordinates[j][0], coordinates[j][1], coordinates[j][2]
                R2 = covalent_R[Z_list[j]]
                R = R1 + R2  # sum of covalent radii
                distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
                if lower_factor * R <= distance <= upper_factor * R:
                    bonds.append([i,j])

        return bonds

    def get_isosurface(self, isoval):
         
        iso = isoval*self.data.max()
        v, f = pg.isosurface(self.data, iso)
        return v, f

    def get_isocolor(self, index):
         
        isocolors = self.settings['isosurface']['colors'].split(',')
        isocolor = isocolors[index].strip()
        color = self.settings['colors'][isocolor]
        return color

    def write_povfile(self, filename):

        self.pov_file = filename
        file = open(filename, 'w')

        self._write_header(file)
        self._write_macros(file)

        if self.domain == 'real':
            self._write_atoms(file)
            self._write_bonds(file)

        if self.isovalues != 'None':
            isovalues = self.isovalues.split(',')
            for i in range(len(isovalues)):
                isovalue = float(isovalues[i])
                v, f = self.get_isosurface(isovalue)
                v[:,0] -= self.grid['nx']/2
                v[:,1] -= self.grid['ny']/2
                v[:,2] -= self.grid['nz']/2
                v[:,0] *= self.grid['dx']
                v[:,1] *= self.grid['dy']
                v[:,2] *= self.grid['dz']

                color = self.get_isocolor(i)
                self._write_isosurface(file, isovalue, v, f, color)

        file.close()

    def run_povray(self, executable='povray'):
        import os
        os.system(executable+' '+self.pov_file)

    def _write_atoms(self, file):

        coordinates = self.molecule['atomic_coordinates']
        Z_list = self.molecule['chemical_numbers']

        print('// Atoms', file=file)
        for Z, xyz in zip(Z_list, coordinates):
            element = number2symbol[Z]
            r, R, G, B, T = self._get_atomsetting(element)
            x, y, z = xyz[0], xyz[1], xyz[2]

            print('a(%g,%g,%g,%g,%g,%g,%g,%g)'%(x,y,z,r,R,G,B,T), file=file)
        print('\n', file=file)


    def _write_bonds(self, file):

        coordinates = self.molecule['atomic_coordinates']
        Z_list = self.molecule['chemical_numbers']
        print('// Bonds', file=file)
        for bond in self.bonds:
            i, j = bond[0], bond[1]
            Z1, Z2 = Z_list[i], Z_list[j]
            element1, element2 = number2symbol[Z1], number2symbol[Z2]

            if self.settings['bonds']['color'] == 'automatic':
                r1, R1, G1, B1, T1 = self._get_atomsetting(element1)
                r2, R2, G2, B2, T2 = self._get_atomsetting(element2) 
                x1, y1, z1 = coordinates[i][0], coordinates[i][1], coordinates[i][2]
                x2, y2, z2 = coordinates[j][0], coordinates[j][1], coordinates[j][2] 
                xm, ym, zm = 0.5*(x1+x2), 0.5*(y1+y2), 0.5*(z1+z2)
                radius = float(self.settings['bonds']['radius'])

                print('b(%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g)'
                        %(x1,y1,z1,radius,xm,ym,zm,radius,R1,G1,B1,T1), file=file)
                print('b(%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g)'
                        %(xm,ym,zm,radius,x2,y2,z2,radius,R2,G2,B2,T2), file=file)                

        print('\n', file=file)

    def _write_isosurface(self, file, isovalue, vertices, faces, color):

        print('//Isosurface for isovalue = %g'%isovalue, file=file)

        if len(vertices) >= 3:
            print('mesh2 { \n vertex_vectors { %i'%len(vertices), file=file)
            for v in vertices:
                print(',<%g,%g,%g>'%(v[0], v[1], v[2]), file=file)
            print('}', file=file)

            print('texture_list { 1, texture{pigment{rgbt<%s>} translucentFinish(0)} }'%color,file=file)

            print('face_indices { %i'%len(faces),file=file)
            for f in faces:
                print(',<%i,%i,%i>, 0,0,0'%(f[0], f[1], f[2]), file=file)    
            print('}', file=file)
            print('}\n', file=file)


    def _get_atomsetting(self, element):

            if element in self.settings['atoms'].keys():
                setting = self.settings['atoms'][element]

            else:
                setting = self.settings['atoms']['default']

            words = setting.split(',')
            r = float(words[0]) # radius
            if len(words) > 2: # color specified as RGBT
                R = float(words[1]) # red
                G = float(words[2]) # green
                B = float(words[3]) # blue
                T = float(words[4]) # transparency

            else:
                color = self.settings['colors'][words[1].strip()].split(',')
                R = float(color[0]) # red
                G = float(color[1]) # green
                B = float(color[2]) # blue
                T = float(color[3]) # transparency

            return r, R, G, B, T


    def _write_header(self, file):

        print("""
#version 3.7;
#declare Width = 500;
#declare Height = 500;
#declare minScreenDimension = 500;
#declare noShadows = false;
""", file=file)

        # camera settings, background and light
        if self.settings['camera']['perspective']=='True':
            perspective = 'perspective'
        else:
            perspective = ''

        location = self.settings['camera']['location']
        look_at = self.settings['camera']['look_at']

        print('camera{ \n %s location \n %s \n look_at %s'
             %(perspective, location, look_at), file=file )

        keywords = ['right', 'up', 'sky', 'angle']
        for keyword in keywords:
            if keyword in self.settings['camera'].keys():
                value = self.settings['camera'][keyword]
                print('%s %s'%(keyword, value), file=file)

        print('}', file=file)

        # background
        rgb = self.settings['background']['rgb']
        print('background { color rgb %s }'%(rgb), file=file)

        # light_source
        position = self.settings['light_source']['position']
        rgb = self.settings['light_source']['rgb']
        print('light_source {%s rgb %s }'%(position, rgb), file=file)



    def _write_macros(self, file):

        print("""
#default { finish {
  ambient 0.45
  diffuse 0.84
  specular 0.22
  roughness .00001
  metallic
  phong 0.9
  phong_size 120
}}

#macro check_shadow()
 #if (noShadows)
  no_shadow 
 #end
#end

#declare slabZ = 0;
#declare depthZ = 2147483647;
#declare dzSlab = 10;
#declare dzDepth = dzSlab;
#declare dzStep = 0.001;

#macro translucentFinish(T)
 #local shineFactor = T;
 #if (T <= 0.25)
  #declare shineFactor = (1.0-4*T);
 #end
 #if (T > 0.25)
  #declare shineFactor = 0;
 #end
 finish {
  ambient 0.45
  diffuse 0.84
  specular 0.22
  roughness .00001
  metallic shineFactor
  phong 0.9*shineFactor
  phong_size 120*shineFactor
}#end

#macro a(X,Y,Z,RADIUS,R,G,B,T)
 sphere{<X,Y,Z>,RADIUS
  pigment{rgbt<R,G,B,T>}
  translucentFinish(T)
  check_shadow()}
#end

#macro b(X1,Y1,Z1,RADIUS1,X2,Y2,Z2,RADIUS2,R,G,B,T)
 cone{<X1,Y1,Z1>,RADIUS1,<X2,Y2,Z2>,RADIUS2
  pigment{rgbt<R,G,B,T>}
  translucentFinish(T)
  check_shadow()}
#end
""" 
     ,file=file)


