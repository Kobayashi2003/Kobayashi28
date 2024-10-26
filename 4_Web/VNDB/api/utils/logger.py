import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create file handler which logs even debug messages
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)  # 5 MB per file, keep 5 old versions
    file_handler.setLevel(level)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a logger for db operations
db_logger = setup_logger('db_operations', 'logs/db.log')
# Create a logger for download operations
download_logger = setup_logger('download_operations', 'logs/download.log')
# Create a logger for search operations
search_logger = setup_logger('search_operations', 'logs/search.log')

test_logger = setup_logger('test_logger', 'logs/test.log')