# -*- coding:utf-8 -*-

"""Create logger."""

import logging

DEBUG, INFO, WARNING, ERROR, CRITICAL = (
    'debug', 'info', 'warning', 'error', 'critical',
)

get_log_level = {
    DEBUG: logging.DEBUG,
    INFO: logging.INFO,
    WARNING: logging.WARNING,
    ERROR: logging.ERROR,
    CRITICAL: logging.CRITICAL,
}.get


def init(level=DEBUG):  # noqa: D103
    logging.basicConfig(
        format='%(name)s:%(levelname)s:%(message)s',  # noqa: WPS323
        level=get_log_level(level),
    )


def get(name='page-loader'):  # noqa: D103
    return logging.getLogger(name)
