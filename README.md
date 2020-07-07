# Map
Map is utility project to display, modify and compare momentum maps of
orbitals from ARPES experiments and DFT calculations.


## Author

- Name: Dominik Brandstetter
- Email: dominik.brandstetter@edu.uni-graz.at
- GitHub Page: https://github.com/brands-d


## Installation

Clone the project into a local repository. To do this create a new
folder locally and execute the following command from within:

    git clone https://github.com/brands-d/Map.git
    
or download the .zip file here:

    https://github.com/brands-d/Map/archive/master.zip
    
and extract the project into the local directory.

### Linux

Before the first start execute the install command of the makefile to
install the necessary packages:

    make install
    
### Windows

To install the program please execute the following commands inside
the root directory of the package (the one that contains the README.md file):

	pip install -r requirements.txt
	python setup.py install   
    
## Usage

### Linux
    
    make run
    
### Windows

    python .\map\__main__.py
