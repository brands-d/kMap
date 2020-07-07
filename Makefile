init:
	pip install -r requirements.txt
	#python setup.py install

run:
	python main.py

test-all:
	python -m unittest discover