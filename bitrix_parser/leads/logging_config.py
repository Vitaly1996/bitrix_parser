import logging
import os

from django.conf import settings


def setup_logging():
    log_format = (
        '%(asctime)s - %(message)s'
    )
    log_file = os.path.join(settings.BASE_DIR, 'output.log')

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(logging.Formatter(log_format))

    info_filter = logging.Filter()
    info_filter.filter = lambda record: record.levelno == logging.INFO
    file_handler.addFilter(info_filter)

    logger = logging.getLogger()
    logging.getLogger().addHandler(file_handler)
    logger.setLevel(logging.INFO)


setup_logging()
