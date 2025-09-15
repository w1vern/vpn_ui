
import logging
import sys

from shared.config import BootLevel, env_config

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    level=logging.INFO if env_config.boot_level is BootLevel.RELEASE else logging.DEBUG,
                    handlers=[logging.StreamHandler(sys.stdout)])


def setup_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)
