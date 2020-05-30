#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import argparse
import logging
import sys

import requests

import page_loader

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


def get_parser():  # noqa: D103
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
        default=ERROR,
        choices=[
            DEBUG,
            INFO,
            WARNING,
            ERROR,
            CRITICAL,
        ],
        help='set loggin level (default: {0})'.format(ERROR),
    )
    return parser


def main():  # noqa: WPS213
    """Run main function."""
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(
        format='%(levelname)s:%(message)s',  # noqa: WPS323
        level=get_log_level(args.logging),
    )

    logging.debug(args.url)
    logging.debug(args.output)

    try:
        page_loader.load(args.url, args.output)

    except requests.exceptions.RequestException as request_e:
        logging.error('Connection error. {0}'.format(str(request_e)))
        sys.exit(1)

    except FileNotFoundError:
        logging.error('The output directory does not exist.')
        sys.exit(1)

    except PermissionError:
        logging.error('Permission denied: {0}'.format(args.output))
        sys.exit(1)


if __name__ == '__main__':
    main()
