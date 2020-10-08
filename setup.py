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
      include_package_data=True)
