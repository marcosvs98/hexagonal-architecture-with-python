import logging
from settings import ENV_SERVER


def get_logger():
    logger = logging.getLogger('json')
    if ENV_SERVER == 'LOCAL':
        logger = logging.getLogger('root')

    return