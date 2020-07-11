# Map
Map is utility project to display, modify and compare momentum maps of
orbitals from ARPES experiments and DFT calculations.


## Author

- Name: Dominik Brandstetter
- Email: dominik.brandstetter@edu.uni-graz.at
- GitHub Page: https://github.com/brands-d


## Installation

Before installing Map please make sure you have a python version of 3.7
or higher installed.
With this you should have pip already installed. If not please install
it using this guide (https://pip.pypa.io/en/stable/installing/)

If you don't have virtualenv already installed, please do so with the
following command:

    pip install virtualenv

Clone the project into a local repository. To do this execute the
following command for https:

    git clone https://github.com/brands-d/Map.git

or if you have a ssh connection setup:

    git clone git@github.com:brands-d/Map.git

Alternatively, if don't have git installed (i.e. using Windows) you can
download the .zip file here:

    https://github.com/brands-d/Map/archive/master.zip
    
and extract the project into the local directory.

### Linux

To install (or update if you downloaded a newer version of Map) just
execute

    make install
    
This will create a virtual python enviroment, installs all the necessary
dependencies and installs Map itself. Afterwards please run

    make test-all

to test all modules and check if they come back passing.

### Windows & MacOS

First create a new virtual enviroment using

    python -m venv venv

in which we install all necessary dependencies

    python -m pip install -r requirements.txt

Next install the Map program itself

    python setup.py install

and last but not least run the test to check if everything works as intended

    python -m unittest discover

## Usage

### Linux
    
    make run
    
### Windows & MacOS

    python ./map/map.py
