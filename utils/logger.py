import logging
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(name)s - %(message)s','%Y-%m-%d %H:%M:%S'))
        logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger
