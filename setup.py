from setuptools import setup, find_packages
from kmap import __version__

setup(
    name="kMap",
    version=__version__,
    description="Display, modify and analyse ARPES experiments and DFT \
      simulations.",
    packages=find_packages(),
    license="LGPL",
    url="https://github.com/brands-d/kMap",
    author="Dominik Brandstetter",
    author_email="brandstetter.dominik@uni-graz.at",
    zip_safe=False,
    install_requires=[
        "h5py",
        "scipy",
        "matplotlib",
        "pyside6",
        "numpy",
        "pyopengl",
        "lmfit",
        "pyqtgraph>=0.13.3",
        "scikit-image",
    ],
    include_package_data=True,
)
