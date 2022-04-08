"""python log script"""
import logging
from logging import config
from random import randint
from time import sleep

from loggers import ErrorLoggerDict, ErrorLogger

# ErrorLoggerDict()
ErrorLogger()
# config.fileConfig('logger.conf')


def main():
    """
    long script main method
    """
    while True:
        i = randint(1, 10)
        # trigger a crash if we get a 10
        if i == 10:
            logging.error('Generated %d. Application Crashing', i)
            raise Exception('Application Crashing')
        logging.info('Generated %d. Sleeping', i)
        sleep(1)


if __name__ == "__main__":
    print('Starting the simple test application')
    main()
