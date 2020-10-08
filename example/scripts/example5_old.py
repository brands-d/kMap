# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Minimizer, Parameters, report_fit

# kMap.py Imports
from kmap.library.orbital import Orbital
from kmap.library.sliceddata import SlicedData
from kmap.library.misc import step_size_to_num

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

# define common (kx,ky)-grid for deconvolution
k_range, dk = [-3.0, 3.0], 0.04
num = step_size_to_num(k_range, dk)
kx = np.linspace(k_range[0], k_range[1], num)
ky = kx

# read PTCDA orbitals from file and compute kmaps
names = ['PTCDA_C', 'PTCDA_D', 'PTCDA_E', 'PTCDA_F', 'background']
styles = ['.r-', 'k-', 'r--', '^g-', 'k:']
params = Parameters()  # parameters object for minimization

sim_kmaps = []
for name in names[:-1]:
    # read cube-file from file
    cuberead = open(data_path / (name + '.cube')).read()
    orbital = Orbital(cuberead, dk3D=0.12)     # 3D-FT
    sim_kmap = orbital.get_kmap(E_kin=27.2,
                                dk=(kx, ky),
                                phi=0, theta=0, psi=0,  # Euler angles
                                Ak_type='toroid',     # toroidal analyzer
                                polarization='p',     # p-polarized light
                                alpha=40)             # angle of incidence
    # sim_kmap.interpolate(kx,ky,update=True)
    sim_kmaps.append(sim_kmap)
    params.add(name, value=1, min=0)   # fit parameter weight of orbital

# also use constant background as fit parameter
params.add('background', value=1, min=0)

# Load experimental data-file: ARPES data of M3-feature of PTCDA/Ag(110)
exp_data = SlicedData.init_from_hdf5(data_path / 'example5_6584.hdf5')

# define function to be minimized


def chi2_function(params, data):
    p = params.valuesdict()
    sum_sim_kmap = np.zeros_like(data)
    for i, weight in enumerate(p):
        if weight != 'background':
            sum_sim_kmap += p[weight] * sim_kmaps[i].data
    difference = sum_sim_kmap - (exp_kmap.data - p['background'])
    return difference


# main program
nslice = exp_data.data.shape[0]
pDOS = np.zeros((nslice, len(names)))
for i in range(nslice):
    exp_kmap = exp_data.slice_from_index(i)  # get kmap slice from exp. data
    # interpolate to common (kx,ky)-grid
    exp_kmap.interpolate(kx, ky, update=True)
    minner = Minimizer(chi2_function, params, fcn_kws={
                       'data': exp_kmap.data}, nan_policy='omit')
    result = minner.minimize()
    pdir = result.params.valuesdict()
    for j, p in enumerate(pdir):
        pDOS[i, j] = pdir[p]
#    report_fit(result)

print(pDOS)

# plot results: weights of orbitals (pDOS) vs. kinetic energy
fig, ax = plt.subplots(figsize=(12, 5))
x = exp_data.axes[0].axis
x_label = exp_data.axes[0].label + '(' + exp_data.axes[0].units + ')'
for j, p in enumerate(names):
    ax.plot(x, pDOS[:, j], styles[j], label=p)
plt.legend()
plt.xlabel(x_label)
plt.ylabel('weights (arb. units)')
# plt.savefig('Fig6_deconvolution.png',dpi=300)
plt.show()
