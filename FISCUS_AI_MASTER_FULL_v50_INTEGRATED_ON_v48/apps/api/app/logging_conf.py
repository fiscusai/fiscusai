import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s | %(message)s")

    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Rotating File
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
