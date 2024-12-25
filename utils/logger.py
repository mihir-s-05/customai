import logging
import os
from config import LOG_LEVEL, LOG_FILE

# Ensure the logs directory exists
LOG_DIR = os.path.dirname(LOG_FILE)
if LOG_DIR and not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str):
    """
    Create and configure a logger with both file and console handlers.

    Args:
        name (str): The name of the logger (usually `__name__`).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Create the main logger
logger = get_logger(__name__)
