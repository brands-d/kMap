.SILENT: ;

setup:
	rm -rf venv build dist *.egg-info
	python -m venv venv
	python -m pip install -r requirements.txt
	python setup.py install

clean:
	rm -rf build dist *.egg-info

run:
	python -m map

test-all:
	python -m unittest discover

# Pleae don't use unless you know what you are doing
freeze:
	pip freeze > requirements.txt

# Pleae don't use unless you know what you are doing
include-config:
	git update-index --no-skip-worktree map/resources/config/*

# Pleae don't use unless you know what you are doing
exclude-config:
	git update-index --skip-worktree map/resources/config/*

help:
	echo 'Usage:'   
	echo '    make <command> [options]'
	echo 'Commands:'
	echo '    setup        Sets up a venv and installs the program.'
	echo '    clean        Removes dist and build directories.'
	echo '    run          Starts the application.'
	echo '    test-all     Runs all available tests.'