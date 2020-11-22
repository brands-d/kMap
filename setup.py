from setuptools import setup, find_packages
from kmap import __version__

pyqtgraph = 'pyqtgraph @ git+ssh://git@github.com/pyqtgraph/pyqtgraph@abfac52c34e368171db472efc8efc581b6383f0d#egg=pyqtgraph'
setup(name='kMap',
      version=__version__,
      description='Display, modify and analyse ARPES experiments and DFT \
      simulations.',
      packages=find_packages(),
      license='MIT',
      url='https://github.com/brands-d/kMap',
      author='Dominik Brandstetter',
      author_email='dominik.brandstetter@edu.uni-graz.at',
      zip_safe=False,
      install_requires=['h5py==2.10.0', 'scipy==1.5.1',
                        'matplotlib==3.3.0', 'numpy==1.19.0',
                        'PyQt5==5.15.0', 'PyOpenGL==3.1.5',
                        'lmfit==1.0.1', pyqtgraph],
      include_package_data=True)
