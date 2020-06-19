# -*- coding:utf-8 -*

"""Args parser module."""

import argparse

from page_loader.lib import log_level


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
        default=log_level.ERROR,
        choices=[
            log_level.DEBUG,
            log_level.INFO,
            log_level.WARNING,
            log_level.ERROR,
            log_level.CRITICAL,
        ],
        help='set loggin level (default: {0})'.format(log_level.ERROR),
    )

    return parser
