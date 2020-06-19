# -*- coding:utf-8 -*

"""Logging levels."""

import logging

DEBUG, INFO, WARNING, ERROR, CRITICAL = (
    'debug', 'info', 'warning', 'error', 'critical',
)

get = {
    DEBUG: logging.DEBUG,
    INFO: logging.INFO,
    WARNING: logging.WARNING,
    ERROR: logging.ERROR,
    CRITICAL: logging.CRITICAL,
}.get
