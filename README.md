# kMap.py
kMap.py is a python based program for simulation and data analysis in photoemission tomography. The underlying theoretical methodology is described in the following publication:

Dominik Brandstetter, Xiaosheng Yang, Daniel Lüftner, F. Stefan Tautz, and Peter Puschnig, "kMap.py: A Python program for simulation and data analysis in photoemission tomography", Computer Physics Communications, available online (2021) https://doi.org/10.1016/j.cpc.2021.107905

Please cite this work when using results from kMap.py in your publications.

It provides an easy-to-use graphical user interface powered by PyQt5 to simulate photoemission momentum maps of molecular orbitals and to perform a one-to-one comparison between simulation and experiment. For this kMap.py provides tools like line- or region-restricted intensity scans/plots, interpolation capabilities, adjustable simulation parameters (like orientation, final state kinetic energy and polarization state of the incident light field) as well as an interface to powerful least-square fits between simulation and experiment to quickly determine optimal parameters.

GitHub Page: https://github.com/brands-d/kMap

## Authors
- Peter Puschnig, Assoz. Prof. Dipl.-Ing. Dr. (peter.puschnig@uni-graz.at)
- Dominik Brandstetter, MSc. (dominik.brandstetter@uni-graz.at)


## Quick-Start

Installation:

    pip install kMap

Usage:

    python -m kmap

## Pre-packaged distribution (Windows 10 only)

A built distribution for an old kMap verison is available on request for Windows 10 in form of a .zip file. For this, please send an email to peter.puschnig(at)uni-graz.at.
To use this version of kMap, please unzuip the file, enter the resulting folder and double click the kMap.exe file.

## Detailed installation guide from source

The installation is mostly done via make commands. Because Windows does not support Makefiles natively, this installation guide will differ between Linux and Windows at multiple points. Please follow the part corresponding to your operating system. For Mac users: As MacOS natively support bash, the Linux guide should work fine.

### 1. Install Python
Before installing kMap.py, please make sure you have a python version of 3.8 or higher installed. If not, you can get one here

    https://www.python.org/downloads/

With this, you should have pip already installed. If not please install it using this guide (https://pip.pypa.io/en/stable/installing/).

Note: If you are using Python 3.7 you might need to install importlib_metadata manually using:
    pip install importlib_metadata
    
### 2. Clone Git Project
Clone the project into a local repository. If you have git installed, simply execute the following command for https:

    git clone https://github.com/brands-d/kMap.git

or if you have an ssh connection set up:

    git clone git@github.com:brands-d/kMap.git

Alternatively, if don't have git installed you can download the .zip file here:

    https://github.com/brands-d/kMap/archive/master.zip
    
and extract the project into the local directory.

### 3. Virtual environment
It is recommended to use a virtual environment to run kMap.py in. If you are using Anaconda or are familiar with venv, please set up a new environment and activate it. Then skip ahead to section 5. Installation. If you don't want to utilize a virtual environment at all, please also skip ahead to section 5. Installation.

To use a virtual environment please check if you have virtualenv already installed. If not please do so with the following command:

    pip install virtualenv

#### Linux
The following commands will set up a virtual environment inside the kMap's root directory
    
    make setup

#### Windows
Please execute the following commands. If your shell does not recognize the "rm" command, replace "rm" with "del".

    rm -rf venv build dist *.egg-info
    python -m venv venv

### 4. Activate Enviroment
The environment is set up but needs to be activated manually. ATTENTION: You will need to reactivate the environment for every new shell again. Please follow this point to do so.

#### Linux
    source ./venv/bin/activate
    
#### Windows
    .\venv\Scripts\activate

To deactivate the environment simply call (both operation systems)

    deactivate
    
### 5. Installation
If you skipped section 3. and 4. please make sure you are in the environment you want the packages to be installed in. Additionally, please make sure you are using the latest version of pip as PyQt5 is known to have trouble with older versions. You can (should) upgrade pip using

    pip install --upgrade pip

If you want to have more control over what is happening, please follow the "Manually" section.

The following commands will install kMap.py and all necessary packages inside

#### Linux 
    make install

#### Windows
    python setup.py install

### 5. Testing
Last please run the tests to check if they come back passing.

#### Linux
    make test-all

### Windows
    python -m unittest discover

It should say something like "OK" at the end. If you see "FAILED" one or more tests came back negative. If that's the case please make sure you installed kMap.py correctly and retry. If it still fails, please contact one of the authors.

## Configuration
All configuration files can be found in ./kmap/config. Each configuration file (logging, settings and shortcut) exists in two different versions (xxx_user.ini and xxx_default.ini). DO NOT edit the default version. You can lose all your settings when updating. Instead, copy any settings you want to change into the respective user file and change it there. The user file does not have to contain all settings, but only those you want to be changed.

This can be done inside the GUI under the "Preferences" menu. "Reload Settings" reloads the settings at runtime. Most settings (not all of them) can be changed at run time this way.

Recommended settings to customize:
app - Customize the size the app starts in depending on your resolution.
paths - Customize the search path for data for quicker access.

## Usage
Before running, make sure you are in the correct environment in which you installed kMap.py. If you decided to use the venv kMap.py comes with, this corresponds to 4. Activate Environment.

To start kMap.py simply run

    python -m kmap

Tutorial videos demonstrating the most important features of kMap.py can be found here: https://www.youtube.com/playlist?list=PLAoZOqtibC5ypO57SU4emdelPzSGQRO8c 

## Updating
Major releases for kMap.py are distributed via the PyPI Server (pip install). The source code and all minor updates with it are hosted on GitHub (https://github.com/brands-d/kMap). If you cloned the project using git executing

    git pull origin master

will update the project to the most recent release.
If you downloaded the .zip file in section 2. Clone Git Project manually, please download it again from the GitHub page and follow the installation instructions. Copy and replace your user settings files from the old version to the new version.

The project is currently structured into a "master" branch (release), a "dev" branch (beta) and various working branches (experimental) usually named after the person working on it. It is not recommended to clone from those branches. 
    
## Bug Report
Bug reports are highly appreciated. Please first run the

    make report

command (only Linux, no equivalent for Windows currently). This will create a report.tar.gz file containing relevant files like the log files and your settings. Please add this file to any bug report! (Windows: Until an easy solution is added please attach the log file (default.log) to your bug report). Please note that this process might take a while since all tests will be run.

Simply send this file via E-mail to one of the authors
(dominik.brandstetter@edu.uni-graz.at).

## Troubleshooting

A list of problems users had before and how they solved it:

### Ubuntu (LTS 20.04)
#### ImportError: /lib/x86_64-linux-gnu/libQt5Core.so.5: version 'Qt_5.15' not found
    pip install pyqt5 --force-reinstall --no-cache

### Anaconda
#### No frame on the MainWindow or libEGL warning: MESA-LOADER: failed to open iris: /usr/lib/dri/iris_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
At the following to your .bashrc or whatever shell you are using. (see [here](https://stackoverflow.com/questions/71010343/cannot-load-swrast-and-iris-drivers-in-fedora-35/72200748#72200748))
    
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

### Windows
#### ImportError: DLL load failed while importing QtGui: The specified procedure could not be found.
Origin is not clear. Make sure you have python 3.8.x installed (not 3.7) and force reinstall PyQt5 in your enviroment:
    pip uninstall pyqt5
    pip install pyqt5 --force-reinstall --no-cache

## Project Structure
The root folder of the kMap.py source code should contain after successful installation at least the following files and directories:
- /dist
- /docs
- /example
- /kmap
- .gitignore
- LICENSE.md
- Makefile
- README.md
- Manifest.in
- setup.py

### /dist
Contains the distribution versions of major releases in wheel and tar.gz form.

### /docs
The /docs subdirectory contains documentation regarding the project. This includes a style guide, class- and package-diagrams as well as a description of the .hdf5 file structure.

### /example
The /example subdirectory contains example data (/example/data) and example scripts (/example/scripts). The scripts are both a show-off what is possible and a tutorial of how to do various things with kMap.py. Check out the file /example/scripts/README for further information.

### /kmap
This is the main folder for the program itself. It contains all the code and tests split into the following subdirectories:
- /config
- /controller
- /library
- /model
- /resources
- /tests
- /ui

The source code roughly follows the MVC (model-view-controller) design pattern. However, due to various reasons, this separation is not strictly followed all the time.

#### /config
This directory contains all the configuration files as well as the "config" class responsible for loading, parsing and providing the settings throughout the rest of the program.

#### /controller
This directory contains all the controller classes and is somewhat the heart of the kMap.py program.

Pretty much every feature/GUI element has its own controller class. Controller classes (as in MCV) contain everything not suited or possible in model classes or .ui files. They handle the interaction with other elements, signals/slots, creation and destruction, some necessary GUI editing as well as quick and minor calculations.

#### /library
This directory contains various base classes.

The most important classes are:
- misc.py: This file contains various general methods and useful methods used at different parts of kMap.py.
- orbital.py: This class is responsible for loading .cube files, calculating momentum maps from the simulation data and providing an easy interface to other parts of the program.
- plotdata.py: All image-like data plotted in kMap.py is based on this class. It provides additional core attributes (like axis information) and core functionality like interpolation and smoothing.
- sliceddata.py : This class defines sliced-data as a 3D data set with axis information usually constructed out of .hdf5 experimental data.

#### /model
This directory contains model classes (as in MCV) for various more complex controller classes.

Model classes encapsulate more complex handling of data from the more general organisational matters dealt with by the controller classes themselves. They are completely removed from handling GUI elements or interacting with other elements and only get, store, edit and provide an interface to data. Therefore most controller classes don't need such a model class.

#### /resources
This directory contains different types of additional resources for the program to run (like the icon image file).

#### /tests
This directory contains all the tests available.

Each file contains one or more test classes based on the unittest module. Run them through the "make test-all" command or individually by "python -m unittest kmap/tests/xxx" where "xxx" denotes the file containing the class you want to test.

#### /ui
This directory contains all the .ui files exported by QtCreator and imported and parsed by the classes in the /controller directory.

The .ui files represent the view part in the MVC pattern. They are auto-generated by QtCreator, a program with an open-source license option to easily and simply create Qt-based GUIs. The files are written in a .xml format and can be opened, viewed and edited by the QtCreator program.

With some exceptions, all GUI related things are defined here (in QtCreator).
