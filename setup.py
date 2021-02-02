from setuptools import setup, find_packages
from kmap import __version__

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
      install_requires=['h5py>=3.1.0', 'scipy>=1.5.1',
                        'matplotlib>=3.3.0', 'numpy>=1.19.0,!=1.19.4',
                        'PyQt5>=5.15.0', 'PyOpenGL>=3.1.5',
                        'lmfit>=1.0.1', 'pyqtgraph>=0.11.0',
                        'qdarkstyle>=2.8.1'],
      include_package_data=True)
