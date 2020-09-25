# example scripts for kMap
All example and demo scripts in this folder can be excecuted from the command line, e.g.:

> python example0.py

Scripts example1.py, example2.py, example3.py, example4.py and example5.py 
produce images that can be directly compared with the Figures published in the
paper accompanying this program [1].

## example0.py
This script computes kmaps of pentacene's HOMO for various kinetic energies and
produces a graph with momentum maps for E_kin = 10, 20, 30, 50, 75 and 100 eV.
The cube-file for the pentacene HOMO is read from example/data/pentacene_HOMO.cube
and the get_kmap() method of the Orbital class from kmap.library.orbital is used
to create the momentum maps. 

The following arguments can be passed to get_kmap() with default values given:

    keyword-arg    default  description
-----------------------------------------------------------------------------------------
    E_kin          30.0     Kinetic energy in eV.
    dk             0.03     Desired k-resolution in kmap in Angstroem^-1.
    phi            0.0      Euler orientation angle phi in degree.
    theta          0.0      Euler orientation angle theta in degree.
    psi            0.0      Euler orientation angle psi in degree.
    Ak_type        'no'     Treatment of |A.k|^2: either 'no','toroid',
                              'NanoESCA', 'only-toroid' or 'only-NanoESCA'.
    polarization   'p'      Either 'p', 's', 'unpolarized', 
                               'C+', 'C-' or 'CDAD'.   
    alpha          0.0      Angle of incidence plane in degree.
    beta           0.0      Azimuth of incidence plane in degree.
    gamma          0.0      Damping factor for final state in
                              Angstroem^-1. str = 'auto' sets gamma automatically
    symmetrization 'no'     either 'no', '2-fold', '2-fold+mirror',
                             '3-fold', '3-fold+mirror','4-fold', '4-fold+mirror'


## example1.py
On the example of the pentacene HOMO (example/data/pentacene_HOMO.cube), this script
demonstrates the calculation of momentum maps for various molecular orientations
using the get_kmap() method of the Orbital class from kmap.library.orbital.

The three resulting momentum maps correspond to Figure 3 (a), (b) and (c) of Ref. [1], 
respectively, with a kinetic energy of 30 eV and the following set of Euler angles:

left panel:   phi = 30°, theta =  0°, psi = 0°

middle panel: phi = 30°, theta =-45°, psi = 0°

right panel:  phi = 90°, theta =-45°, psi =60° 

## example2.py
On the example of the pentacene HOMO (example/data/pentacene_HOMO.cube), this script
demonstrates the treatment of the polarization factor (|A.k|^2) when 
using the get_kmap() method of the Orbital class from kmap.library.orbital.

The three resulting momentum maps correspond to Figure 4 (a), (b) and (c) of Ref. [1].

left panel:   p-polarized light according to Eq. (17) of Ref.[1] for an angle of
			  incidence of alpha=45° and an azimuth of incidence of beta=60°

middle panel: s-polarized light according to Eq. (18) of Ref.[1] for an angle of
			  incidence of alpha=45° and an azimuth of incidence of beta=60°

right panel:  p-polarized light according to Eq. (19) of Ref. [1] for and angle of
  		      incidence of alpha=45° with the incidence and emission planes identical
  		      for all azimuths ("toroidal electron energy analzer with azimuthal rotation
  		      of sample")

## example3.py
On the example of the pentacene HOMO (example/data/pentacene_HOMO.cube), this script
demonstrates the symmetrization of momentum maps. Four momentum maps for molecular
tilt angles of theta=0°, 10°, 20° and 30° degree are computed and symmetrized using
the symmetrization='2-fold' option in get_kmap()

## example4.py
On the example of the tilt-angle of pentacene in a crystalline multi-layer film [2], 
example4.py demonstrates how the the lmfit module is used to peform a least-square
minimization to determine an optimal molecular orientation. More details about
this example can be found in Section 4.1 of Ref. [1].


## example5.py
On the example of the so-called 'M3-feature' of a monoloayer of PTCDA/Ag(110), 
example5.py demonstrates the deconvolution of experimental ARPES data into
individual orbital contributions according to Ref. [3]. More deatils about
this example can be found in Section 4.2 of Ref. [1]


# References

[1] Dominik Brandstetter, Xiaosheng Yang, Daniel Lüftner, and Peter Puschnig
"kMap.py: A python based program for simulation and data analysis in photoemission tomography",
submitted to Computer Physics Communications.

[2] P. Puschnig et al., 
"Reconstruction of Molecular Orbital Densities from Photoemission Data",
Science 326, 702-706 (2009). [doi: 10.1126/science.1176105]

[3] P. Puschnig et al., 
"Orbital tomography: Deconvoluting photoemission spectra of organic molecules",
Phys. Rev. B 84, 235427 (2011) [doi: 10.1103/PhysRevB.84.235427]

