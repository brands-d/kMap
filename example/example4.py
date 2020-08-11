import matplotlib.pyplot as plt
import numpy as np
from lmfit import Minimizer, Parameters, report_fit

# for local imports include parent path
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

# now import classes from kMap
from kmap.library.orbital import Orbital
from kmap.library.sliceddata import SlicedData

# Load experimental data-file and choose a constant-binding energy slice
exp_data = SlicedData.init_from_hdf5('example4.hdf5') 
exp_kmap = exp_data.slice_from_index(5)   # returns PlotData object
kx       = np.arange(-3.0,3.0,0.05)
ky       = kx
exp_kmap.interpolate(kx,ky,update=True)

# create a set of parameters to be minimized
params = Parameters()
params.add('theta',     value=10, min=0, max=90)  # tilting angle of molecule
params.add('weight',    value=1,  min=0)          # weight of orbital
params.add('background',value=0,  min=0)          # constant background

# read pentacene HOMO cube-file from file 
cubefile = open('pentacene_HOMO.cube').read() # read cube-file from file
homo     = Orbital(cubefile,dk3D=0.15)        # 3D-FT 

def chi2_function(params):

    theta      = params['theta']
    weight     = params['weight']
    background = params['background']

    # simulate momentum map for given theta
    sim_kmap = homo.get_kmap(E_kin=28,     
                   phi=90,theta=theta,psi=90,  # Euler angles 
                   Ak_type='toroid',           # toroidal analyzer 
                   polarization='p',           # p-polarized light
                   alpha=60,                   # angle of incidence
                   symmetrization='2-fold')    # symmetrize kmap

    # Interpolate simulated k-maps to the same (kx,ky)-grid as experimental map
    kx = exp_kmap.x_axis
    ky = exp_kmap.y_axis
    sim_kmap.interpolate(kx,ky,update=True)

    difference = (exp_kmap.data - background) - weight*(sim_kmap.data)
 
    return difference

# main program
minner = Minimizer(chi2_function, params, nan_policy='omit')
result = minner.minimize()
report_fit(result)


