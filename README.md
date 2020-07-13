# Map
Map is a utility project to display, modify and compare momentum maps of
orbitals from ARPES experiments and DFT calculations.


## Author

- Name: Dominik Brandstetter
- Email: dominik.brandstetter@edu.uni-graz.at
- GitHub Page: https://github.com/brands-d


## Installation

### 1. Install Python
Before installing Map, please make sure you have a python version of 3.7
or higher installed. If not, you can get one here

    https://www.python.org/downloads/

With this, you should have pip already installed. If not please install
it using this guide (https://pip.pypa.io/en/stable/installing/)

### 2. Clone Git Project
Clone the project into a local repository. If you have git installed,
simply execute the following command for https:

    git clone https://github.com/brands-d/Map.git

or if you have an ssh connection setup:

    git clone git@github.com:brands-d/Map.git

Alternatively, if don't have git installed (i.e. using Windows) you can
download the .zip file here:

    https://github.com/brands-d/Map/archive/master.zip
    
and extract the project into the local directory.

### 3. Virtual environment
Map comes with a complete setup of a virtual environment for Map only
which is the cleanest and safest option to use. This, however,
reinstalls packages you might already have in a distinct directory
which can take up some space (currently about 170MB).
If you want to keep storage Map takes up down, or prefer using our own
environment or program (like conda) you can skip 3. and 4. entirely.

If you don't have virtualenv already installed, please do so with the
following command:

    pip install virtualenv

#### Linux & MacOS (probably)
The following commands will set up a venv folder inside the Map's root
directory
    
    make setup

#### Windows
Windows doesn't come with make installed. Therefore, you have to execute
the commands manually

    rm -rf venv build dist *.egg-info
    python -m venv venv

### 4. Activate Enviroment
Next, we need to activate the environment. ATTENTION: You will need to
reactivate the environment for every new shell again. Please follow this
point to do so.

#### Linux & MacOS (probably)

    source ./venv/bin/activate
    
#### Windows

    .\env\Scripts\activate

To deactivate the environment simply call

    deactivate
    
### 4. Installation

If you skipped section 3. please make sure you are in the environment
you want the packages to be installed.

If you want to have more control over what is happening, please
follow the "Manually" section. Recommend only if you know what
you are doing.

#### Linux & MacOS (probably)
The following commands will install Map and all necessary packages
inside
    
    make install

#### Windows
Again Windows users have to do it manually

    python -m pip install -r requirements.txt
    python setup.py install

#### Manually

To have more control over what is happening, please install the
packages necessary manually. You can find a list in the
requirements.txt file. Afterwards, run

    python setup.py install
    
### 5. Testing

Afterwards please run tests to check if they come back passing.

#### Linux

    make test-all

### Windows

    python -m unittest discover


It should say something like "OK" at the end. If you see "FAILED"
one or more test came back negative. If that's the case please make
sure you installed Map correctly and retry. If it still fails, please
contact the author.

## Configuration

All configuration files can be found in ./map/resources/config. They are
outside the index of git, which means you can (and have to) edit and
change them directly.

## Usage

Before running, make sure you are in the correct environment, in which
you installed Map. If you decided to use the venv Map comes with, redo
4. of the installation instruction.

To start Map simply run

### Linux & MacOS (probably)
    
    make run
    
### Windows

    python -m map