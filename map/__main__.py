def main():

    import logging.config
    from os.path import isfile
    from map import abs_directory

    logging_config_path = abs_directory + '/config/loggings.conf'
    logging.config.fileConfig(abs_directory + '/config/loggings.conf')

    print('Start Map.py')


if __name__ == '__main__':
    main()
