# -*- coding:utf-8 -*

"""Module for CLI-args parser."""

import argparse

from page_loader import logger


def get():  # noqa: D103
    parser = argparse.ArgumentParser(description='Download the internet page')
    parser.add_argument('url')
    parser.add_argument(
        '-O',
        '--output',
        type=str,
        help='path to output folder (default: current working directory)',
    )
    parser.add_argument(
        '--logging',
        type=str,
        default=logger.ERROR,
        choices=[
            logger.DEBUG,
            logger.INFO,
            logger.WARNING,
            logger.ERROR,
            logger.CRITICAL,
        ],
        help='set loggin level (default: {0})'.format(logger.ERROR),
    )
    return parser
