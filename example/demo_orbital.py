import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

####
import matplotlib.pyplot as plt
from kmap.library.orbital import Orbital

cubefile = open('pentacene_HOMO.cube').read()

homo    = Orbital(cubefile,dk3D=0.10)
testmap = homo.get_kmap(E_kin=30,phi=10,Ak_type='no')
testmap = homo.change_polarization(Ak_type='NanoESCA')

# plot for testing purposes
limits  = [testmap.range[0,0], testmap.range[0,1], testmap.range[1,0], testmap.range[1,1]]    
plt.figure()
plt.imshow(testmap.data,extent=limits,interpolation='bicubic',origin='lower' )
plt.show()


