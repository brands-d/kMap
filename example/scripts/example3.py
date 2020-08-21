import os, sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path + os.sep + '..' + os.sep + '..' + os.sep)
data_path = path + os.sep + '..' + os.sep + 'data' + os.sep

####
import matplotlib.pyplot as plt
from kmap.library.orbital import Orbital

cubefile = open(data_path + 'pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile,        # compute 3D Fourier transform (see Eqs. 6-11)  
                   dk3D=0.15)       # with a desired k-spacing of dkx = dky = dkz = 0.15 1/Angstroem                           


# plot Figure 5(c): HOMO of pentacene with tilt angles of theta = 0°, 10°, 20° and 30°
fig, _ax = plt.subplots(2,2)
ax       = _ax.flatten() 
thetas   = [0, 10, 20, 30]
for i, theta in enumerate(thetas):
    homo.get_kmap(E_kin=30,              # compute momentum map for E_kin = 30 eV (Eq. 12)
              dk=0.03,                   # desired grid spacing in kmap in 1/Angstroem
              phi=90,theta=theta,psi=0,  # Euler angles 
              Ak_type='toroid',          # p-polarized light according to Eq. (19) 
              polarization='p',
              alpha=45,                  # angle of incidence
              symmetrization='2-fold')   #  symmetrize kmap
    homo.plot(ax[i],title='$\\vartheta=%g^\circ$'%theta)   # plot kmap 


plt.tight_layout()
plt.show()                          # show figure
