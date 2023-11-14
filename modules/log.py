import logging

from . import config

# 使用logger记录日志
log = logging.getLogger("GameWorldNavigation")


def debug(mes):
    if config.__log__:
        log.debug(mes)


def info(mes):
    if config.__log__:
        log.info(mes)


def warning(mes):
    if config.__log__:
        log.warning(mes)


def error(mes):
    if config.__log__:
        log.error(mes)


def critical(mes):
    if config.__log__:
        log.critical(mes)


if __name__ == '__main__':
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    log.critical('Critical message')
