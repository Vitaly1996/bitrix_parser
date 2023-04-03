import logging
import os

from django.conf import settings


def setup_logging():
    log_format = (
        '%(asctime)s - %(message)s'
    )
    log_file = os.path.join(settings.BASE_DIR, 'output.log')
    logging.basicConfig(
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, 'w'),
        ],
    )
    logging.getLogger().setLevel(logging.INFO)


setup_logging()
