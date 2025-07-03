import logging
import os

def setup_logger(name, log_file="logs/app.log", level=logging.INFO):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

logger = setup_logger("VideoAISystem")
