import src.base.config as config

import logging


def configure_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
    pass
