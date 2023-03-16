import logging

logging.basicConfig(level = logging.WARNING,
                    format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s')

logger = logging.getLogger("parent")
logger.setLevel(logging.INFO)
