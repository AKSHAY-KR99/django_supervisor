import logging
from random import randint

from loggers import ErrorLoggerDict, ErrorLogger

ErrorLoggerDict()
# ErrorLogger()

import time

count = 0
while True:
    count = count + 1
    num = randint(1, 5)
    if num == count or count > 10:
        logging.error('Number and count are equal. Application Crashed in the digit %d', count)
        raise Exception('Application Crashing')
    logging.info('Success... %d this prints... Sleeping', count)
    print(str(count) + ". This prints once every 5secs.")
    time.sleep(2)
