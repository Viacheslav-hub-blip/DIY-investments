import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='finance_api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def logging(func):
    def wrapper(*args, **kwargs):
        logger.info(f"was called with {func.__name__}")

    return wrapper
