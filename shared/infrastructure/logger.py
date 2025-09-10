
import logging
import sys

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    level=logging.DEBUG,
                    handlers=[logging.StreamHandler(sys.stdout)])


def setup_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)
