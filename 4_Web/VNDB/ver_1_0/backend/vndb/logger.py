import os
import logging
from logging.handlers import RotatingFileHandler

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

def add_log_entry(level, message, details=None):
    """Function to add a log entry to the database"""
    from vndb import db
    from vndb.database.models import LogEntry
    import uuid

    log_entry = LogEntry(
        id=str(uuid.uuid4()),
        level=level,
        message=message,
        details=details
    )
    db.session.add(log_entry)
    db.session.commit()

logger = setup_logger('logger', 'vndb/logs/info.log')