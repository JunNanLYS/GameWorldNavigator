import logging

from . import config

# 使用logger记录日志
logger = logging.getLogger("GameWorldNavigator")


def debug(mes):
    if config.__log__:
        logger.debug(mes)


def info(mes):
    if config.__log__:
        logger.info(mes)


def warning(mes):
    if config.__log__:
        logger.warning(mes)


def error(mes):
    if config.__log__:
        logger.error(mes)


def critical(mes):
    if config.__log__:
        logger.critical(mes)


if __name__ == '__main__':
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
