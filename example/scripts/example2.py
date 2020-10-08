# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.orbital import Orbital

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

cubefile = open(data_path / 'pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile,        # compute 3D Fourier transform (see Eqs. 6-11)  
                   dk3D=0.15)       # with a desired k-spacing of dkx = dky = dkz = 0.15 1/Angstroem                           

fig, ax = plt.subplots(1,3)         # create empty figure with 3 axes

# plot Figure 4(a): HOMO of pentacene with polarization P_p according to Eq. 17
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              dk=0.03,              # desired grid spacing in kmap in 1/Angstroem
              phi=0,theta=0,psi=0,  # Euler angles phi=0, theta=0, psi=0 
              Ak_type='NanoESCA',   # p-polarized light according to Eq. (17) 
              polarization='p',
              alpha=45,             # angle of incidence
              beta=60)              # azimuth of incidence plane
homo.plot(ax[0])                    # plot kmap in axis 0

# plot Figure 4(b): HOMO of pentacene with polarization P_s according to Eq. 18
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              dk=0.03,              # desired grid spacing in kmap in 1/Angstroem
              phi=0,theta=0,psi=0,  # Euler angles phi=0, theta=0, psi=0 
              Ak_type='NanoESCA',   # p-polarized light according to Eq. (18) 
              polarization='s',
              alpha=45,             # angle of incidence
              beta=60)              # azimuth of incidence plane
homo.plot(ax[1])                    # plot kmap in axis 0

# plot Figure 4(c): HOMO of pentacene with polarization \tilde{P}_p according to Eq. 19
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              dk=0.03,              # desired grid spacing in kmap in 1/Angstroem
              phi=0,theta=0,psi=0,  # Euler angles phi=0, theta=0, psi=0 
              Ak_type='toroid',     # p-polarized light according to Eq. (19) 
              polarization='p',
              alpha=45)             # angle of incidence (incidence plane not necessary)
homo.plot(ax[2])                    # plot kmap in axis 0


plt.tight_layout()
plt.show()                          # show figure
