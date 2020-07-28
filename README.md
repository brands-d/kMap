# kMap
kMap is a utility project to display, modify and compare momentum maps
of orbitals from ARPES experiments and DFT calculations.


## Author

- Name: Dominik Brandstetter
- Email: dominik.brandstetter@edu.uni-graz.at
- GitHub Page: https://github.com/brands-d


## Installation

### 1. Install Python
Before installing kMap, please make sure you have a python version of 3.7
or higher installed. If not, you can get one here

    https://www.python.org/downloads/

With this, you should have pip already installed. If not please install
it using this guide (https://pip.pypa.io/en/stable/installing/)

### 2. Clone Git Project
Clone the project into a local repository. If you have git installed,
simply execute the following command for https:

    git clone https://github.com/brands-d/kMap.git

or if you have an ssh connection setup:

    git clone git@github.com:brands-d/kMap.git

Alternatively, if don't have git installed (i.e. using Windows) you can
download the .zip file here:

    https://github.com/brands-d/kMap/archive/master.zip
    
and extract the project into the local directory.

### 3. Virtual environment
kMap comes with a complete setup of a virtual environment for kMap only
which is the cleanest and safest option to use. This, however,
reinstalls packages you might already have in a distinct directory
which can take up some space (currently about 400MB).
If you want to keep storage kMap takes up down, or prefer using our own
environment or program (like conda) you can skip 3. and 4. entirely.

If you don't have virtualenv already installed, please do so with the
following command:

    pip install virtualenv

#### Linux & MacOS (probably)
The following commands will set up a venv folder inside the kMap's root
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
you want the packages to be installed. Additionally, please make sure
you are using the latest version of pip as PyQt5 is known to have
trouble with older versions. You can (should) upgrade pip using

    pip install --upgrade pip

If you want to have more control over what is happening, please
follow the "Manually" section. Recommend only if you know what
you are doing.

#### Linux & MacOS (probably)
The following commands will install kMap and all necessary packages
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
sure you installed kMap correctly and retry. If it still fails, please
contact the author.

## Configuration

All configuration files can be found in ./kmap/resources/config. They are
outside the index of git, which means you can (and have to) edit and
change them directly.

## Usage

Before running, make sure you are in the correct environment, in which
you installed kMap. If you decided to use the venv kMap comes with, redo
4. of the installation instruction.

To start kMap simply run

### Linux & MacOS (probably)
    
    make run
    
### Windows

    python -m kmap

## Bug Report

Bug reports are highly appreciated. Please first run

    make report

command (only Linux and maybe MacOS, no equivalent for Windows
currently). This will create a report.tar.gz file containing relevant
files like the log files and your settings. Please add this file to any
bug report! (Windows: Until a easy solution is added please attach at
least the log file (default.log) to your bug report).
Please note that this process might take a while since all test will be
run.

Simply send this file via E-mail to author
(dominik.brandstetter@edu.uni-graz.at).