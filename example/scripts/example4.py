# Python Imports
from pathlib import Path

# Third Party Imports
import matplotlib.pyplot as plt
import numpy as np

# kMap.py Imports
from kmap.library.sliceddata import SlicedData
from kmap.library.orbitaldata import OrbitalData
from kmap.model.lmfit_model import LMFitModel

# Path to data folder; replace with your own; use '/' instead of '+'
# when concatenating with strings
data_path = Path(__file__).parent / Path('../data/')

# Load experimental data as SlicedData object
exp_data = SlicedData.init_from_hdf5(data_path / 'example4_3271.hdf5')

# Load orbital for fitting as OrbitalData objects
orbital_paths = ['pentacene_HOMO.cube']
orbitals = [OrbitalData.init_from_file(
            data_path / path, ID) for ID, path in enumerate(orbital_paths)]

# Initialize fit as LMFitModel object
lmfit = LMFitModel(exp_data, orbitals)

# Set common range and delta-k-grid for exp. and sim. kmaps
range_, dk = [-3.0, 3.0], 0.04
lmfit.set_axis_by_step_size(range_, dk)
lmfit.set_polarization('toroid', 'p')
lmfit.set_symmetrization('2-fold')

# Set parameters not intended for fitting to desired value
lmfit.edit_parameter('E_kin', value=28, vary=False)
lmfit.edit_parameter('alpha', value=40, vary=False)
lmfit.set_background_equation('c')

# Activate fitting for background ('c') and all orbital weights and theta
lmfit.edit_parameter('c', value=1, vary=True)  # constant background
for i in [0]:
    lmfit.edit_parameter('w_' + str(i), vary=True)
    lmfit.edit_parameter('theta_' + str(i), min=0, value=5, vary=True)
    lmfit.edit_parameter('phi_' + str(i), value=90, vary=False)
    lmfit.edit_parameter('psi_' + str(i), value=90, vary=False)

# Set slices to be used and perform fit
lmfit.set_slices([2], combined=False)
lmfit.set_fit_method(method='leastsq', xtol=1e-12)

best_fit = lmfit.fit()[0][1]

# Print results of best fit
print('reduced chi^2 = ', best_fit.redchi)
print(best_fit.params['theta_0'])
print(best_fit.params['w_0'])
print(best_fit.params['c'])

# Now make plot of chi^2 vs. theta by looping over a list of
# theta-values, but setting fixing all variables (vary=False) in the fit
lmfit.edit_parameter('w_0', value=best_fit.params['w_0'].value, vary=False)
lmfit.edit_parameter('c', value=best_fit.params['c'].value, vary=False)
theta_values = np.linspace(0, 60, 61)
redchi2_list = []

for theta in theta_values:
    lmfit.edit_parameter('theta_0', value=theta, vary=False)
    fit = lmfit.fit()[0][1]
    redchi2_list.append(fit.redchi)

# Plot reduced chi^2 versus theta
factor = 1e-3  # arbitrary scaling factor for reduced chi^2
redchi2_list = factor * np.array(redchi2_list)
fig, ax = plt.subplots(figsize=(6.5, 5))
ax.plot(theta_values, redchi2_list, 'k-')
print(best_fit.params['theta_0'].value)
ax.plot([best_fit.params['theta_0'].value], [factor * best_fit.redchi], 'ro')
ax.set_xlabel('$\\vartheta (^\circ)$', fontsize=20)
ax.set_ylabel('$\chi^2_{red}$ (arb. units)', fontsize=20)

plt.xticks(fontsize=20)
plt.tick_params('both', length=10, width=2, direction='in',
                which='major')  # width of major ticks
plt.minorticks_on()
plt.tick_params('both', length=5, width=1, direction='in',
                which='minor')  # width of minor ticks
plt.yticks(fontsize=20)
plt.tight_layout()
# plt.savefig('Fig5a_chi2.png',dpi=300)
plt.show()
