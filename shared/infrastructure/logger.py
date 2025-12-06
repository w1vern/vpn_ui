
import logging
import sys

from shared.infrastructure import BootLevel, env_config

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


def setup_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO
                    if env_config.boot_level is BootLevel.RELEASE else logging.DEBUG)
    return logger
