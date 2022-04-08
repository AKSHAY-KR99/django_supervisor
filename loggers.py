""" Logger Module """
import logging
from datetime import datetime
from logging.config import dictConfig

from pythonjsonlogger import jsonlogger


class ErrorLoggerDict:
    """ Dict logger """

    def __init__(self):
        self.logging_config = {}
        self.config()
        self.logger()

    def config(self):
        """ logger function """
        self.logging_config = {
            'version': 1,
            'loggers': {
                '': {
                    'level': 'NOTSET',
                    'handlers': ['debug_console_handler',
                                 'info_rotating_file_handler',
                                 'error_file_handler'],
                },
            },
            'formatters': {
                'debug': {
                    'format': '%(asctime)s - %(levelname)s - %(name)s ::'
                              ' %(message)s'
                },
                'info': {
                    'format': '%(asctime)s - %(levelname)s - %(name)s : '
                              '%(filename)s - (%(lineno)s) :: %(message)s',
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter"

                },
                'error': {
                    'format': '%(asctime)s - %(levelname)s - %(name)s - '
                              '%(process)d :: %(filename)s - (%(lineno)s) '
                              ':: %(message)s',
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter"
                },
            },
            'handlers': {
                'debug_console_handler': {
                    'level': 'DEBUG',
                    'formatter': 'debug',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
                'info_rotating_file_handler': {
                    'level': 'INFO',
                    'formatter': 'info',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': '/home/akshay/Desktop/django_supervisor/log/info.log',
                    'mode': 'a',
                    'maxBytes': 1048576,
                    'backupCount': 10
                },
                'error_file_handler': {
                    'level': 'WARNING',
                    'formatter': 'error',
                    'class': 'logging.FileHandler',
                    'filename': '/home/akshay/Desktop/django_supervisor/log/error.log',
                    'mode': 'a',
                },
            },
        }

    def logger(self):
        """ logger method """
        dictConfig(self.logging_config)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """ custom json formatter"""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


class ErrorLogger:
    """ Error logger using basic logging class methods """

    def __init__(self):
        self.logger = None
        self.config()
        self.logg()

    def config(self):
        """ config logger function"""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.NOTSET)

    def logg(self):
        """ logger function """
        formatter_console = logging.Formatter('%(asctime)s %(levelname)s'
                                              ' %(name)s %(message)s')
        formatter_json = jsonlogger.JsonFormatter('%(timestamp)s %(level)s'
                                                  ' %(name)s %(message)s')
        formatter_custom = CustomJsonFormatter('%(timestamp)s %(level)s '
                                               '%(name)s %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter_console)

        file_handler_err = logging.FileHandler('/home/akshay/Desktop/django_supervisor/log/error.log')
        file_handler_err.setLevel(logging.ERROR)
        file_handler_err.setFormatter(formatter_json)

        file_handler_info = logging.FileHandler('/home/akshay/Desktop/django_supervisor/log/info.log')
        file_handler_info.setLevel(logging.INFO)
        file_handler_info.setFormatter(formatter_custom)

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler_err)
        self.logger.addHandler(file_handler_info)