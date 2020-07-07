install:
	pip install -r requirements.txt
	python setup.py install

run:
	@python map/__main__.py

test-all:
	@python -m unittest discover