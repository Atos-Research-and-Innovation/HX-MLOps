import logging
import datetime
import os
import yaml
from typing import Union


def configure_logger(
    logger: Union[logging.Logger, None] = None, log_dir: str = "logs", suffix: str = "",
) -> logging.Logger:
    """Configure logger to print to log file and stdout both."""
    logger = logger or logging.getLogger()

    # STDOUT logger
    logger.setLevel(logging.DEBUG)
    now = datetime.datetime.now()
    log_format = '%(asctime)s | %(name)s | %(levelname)s: %(message)s'
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    # File logger
    os.makedirs(log_dir, exist_ok=True)
    suffix = suffix or now.strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f'{suffix}.log')
    logfile_handler = logging.FileHandler(log_path)
    logfile_handler.setLevel(logging.DEBUG)
    logfile_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(logfile_handler)
    logger.propagate = False

    return logger