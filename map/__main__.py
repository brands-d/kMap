import logging.config
from map import __directory__


def main():

    logging.config.fileConfig(__directory__ + '/config/logging.conf')

    print('Start Map.py')


if __name__ == '__main__':
    main()
