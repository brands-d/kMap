import logging.config
from map import __directory__


def main():

    logging.config.fileConfig(__directory__ + '/config/logging.conf')
    root_logger = logging.getLogger('root')

    root_logger.info('Starting Map')




if __name__ == '__main__':
    main()
