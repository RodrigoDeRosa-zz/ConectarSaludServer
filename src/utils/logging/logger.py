import logging

from os import makedirs
from os.path import abspath, join, dirname, exists
from logging.handlers import RotatingFileHandler


class Logger:
    LOGGING_FILE_NAME = 'connecting_health.log'
    FORMATTING_STRING = '%(asctime)s - (%(process)d) - %(levelname)s - %(name)s - %(message)s'
    LOGGING_LEVEL = logging.DEBUG
    MAX_BYTES = (1024 ** 2) * 100  # 100MB
    BACKUP_COUNT = 5  # Keep up to connecting_health.log.5

    @classmethod
    def set_up(cls):
        handlers = []
        # File logging handler
        file_name = f'{abspath(join(dirname(__file__), "../../.."))}/logs/{cls.LOGGING_FILE_NAME}'
        # Create file and directory if they don't exist
        cls.__create_file(file_name)
        handlers.append(RotatingFileHandler(file_name, maxBytes=cls.MAX_BYTES, backupCount=cls.BACKUP_COUNT))
        # Console logging handler
        handlers.append(logging.StreamHandler())
        # Configure
        logging.basicConfig(format=Logger.FORMATTING_STRING, level=Logger.LOGGING_LEVEL, handlers=handlers)

    def __init__(self, class_name, session_id=None):
        self._logger = logging.getLogger(class_name)

    def info(self, message):
        self._logger.info(message)

    def error(self, message, exc_info=True):
        self._logger.exception(message, exc_info=exc_info)

    def debug(self, message):
        self._logger.debug(message)

    def warning(self, message):
        self._logger.warning(message)

    @classmethod
    def __create_file(cls, file_name: str):
        dir_name = file_name.replace(f'/{cls.LOGGING_FILE_NAME}', '')
        if not exists(dir_name): makedirs(dir_name)
        if not exists(file_name): open(file_name, 'w').close()
