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

# Load experimental data-file and choose a constant-binding energy slice
exp_data = SlicedData.init_from_hdf5(data_path / 'example4_3271.hdf5') 
exp_kmap = exp_data.slice_from_index(2)   # take slice #2 from exp. data

# define common (kx,ky)-grid for fitting
k_range, dk = [-3.0, 3.0], 0.04
num = step_size_to_num(k_range, dk)
kx = np.linspace(k_range[0],k_range[1],num)
ky = kx
exp_kmap.interpolate(kx,ky,update=True)

# read pentacene HOMO cube-file from file 
cubefile = open(data_path / 'pentacene_HOMO.cube').read() # read cube-file from file
homo     = Orbital(cubefile,dk3D=0.12)        # 3D-FT 


# define function which returns the difference between exp. and simulated k-map
def chi2_function(params):

    theta      = params['theta']
    weight     = params['weight']
    background = params['background']

    # simulate momentum map for given theta
    sim_kmap = homo.get_kmap(E_kin=28,  
    			   dk=(kx,ky),   
                   phi=90,theta=theta.value,psi=90,  # Euler angles 
                   Ak_type='toroid',           # toroidal analyzer 
                   polarization='p',           # p-polarized light
                   alpha=40,                   # angle of incidence
                   symmetrization='2-fold')    # symmetrize kmap

    difference = (exp_kmap.data - background) - weight*(sim_kmap.data)
    
    return difference

# MAIN PROGRAM #####################################################################

# Compute best fit
params = Parameters()
params.add('theta',     value=5,   min=0,max=90)    # tilting angle of molecule
params.add('weight',    value=5000,min=0,max=5000)  # weight of orbital
params.add('background',value=200, min=0,max=500)   # constant background

minner  = Minimizer(chi2_function, params, nan_policy='omit')
result  = minner.minimize(method='leastsq',xtol=1e-12)
N       = result.ndata   # number of data points
n       = result.nvarys  # number of model parameters 
redchi  = result.redchi  # reduced-chi^2 = chi^2/(N-n) 
bestpar = result.params  # best fit parameters
report_fit(result)       # print fit report to console

# now make plot how chi^2 varies with the tilt angle theta
theta_values = np.linspace(0,60,61)
redchi2_list = []  
factor       = 1e-3 # arbitrary scaling factor for chi^2
for theta in theta_values:
    params = Parameters()
    params.add('theta',     value=theta)              # tilting angle of molecule
    params.add('weight',    value=bestpar['weight'].value)      # take from best fit
    params.add('background',value=bestpar['background'].value)  # take from best fit
    diff = chi2_function(params)
    redchi2_list.append(factor*np.nansum(diff**2)/(N - n)) # compute reduced chi^2


# plot reduced chi^2 versus theta
fig, ax = plt.subplots(figsize=(6.5,5))
ax.plot(theta_values,redchi2_list,'k-')
ax.plot([bestpar['theta'].value],[factor*redchi],'ro')
ax.set_xlabel('$\\vartheta (^\circ)$',fontsize=20)
ax.set_ylabel('$\chi^2_{red}$ (arb. units)',fontsize=20)
plt.xticks(fontsize=20)
plt.tick_params('both', length=10, width=2,direction='in',which='major')  # width of major ticks
plt.minorticks_on()
plt.tick_params('both', length=5, width=1, direction='in',which='minor')  # width of minor ticks
plt.yticks(fontsize=20)
plt.tight_layout()
#plt.savefig('Fig5a_chi2.png',dpi=300)
plt.show()


