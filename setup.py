from setuptools import setup, find_packages
from map import __version__

setup(name='Map',
      version=__version__,
      description='Display, modify and analyse ARPES experiments and DFT \
      simulations.',
      install_requires=['python==3.7'],
      packages=find_packages(),
      license='MIT',
      url='https://github.com/brands-d/Map',
      author='Dominik Brandstetter',
      author_email='dominik.brandstetter@edu.uni-graz.at'
      )
