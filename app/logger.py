import logging
from logging.handlers import RotatingFileHandler
import os

def create_logger(name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a file handler and set its level to DEBUG
    max_log_size = 8 * 1024 * 1024
    logs_folder = 'logs'
    os.makedirs(logs_folder, exist_ok=True)  # Create the logs folder if it doesn't exist
    log_file = os.path.join(logs_folder, f'{name}.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('Logger created')
    return logger

logger = create_logger("blur_log")



