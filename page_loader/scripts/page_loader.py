#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import sys

import requests

import page_loader
from page_loader import logger, parser


def main():  # noqa: WPS213
    """Run main function."""  # noqa: DAR401
    args_parser = parser.get()
    args = args_parser.parse_args()

    logger.init(args.logging)
    log = logger.get(__name__)

    log.debug(args.url)
    log.debug(args.output)

    try:
        page_loader.load(args.url, args.output)

    except requests.exceptions.RequestException:
        print('Connection error.')
        sys.exit(1)

    except ValueError as e:  # noqa: WPS111
        if str(e) == 'Page not found.':
            print(str(e))
            sys.exit(1)
        else:
            raise

    except FileNotFoundError:
        print('The output directory does not exist.')
        sys.exit(1)


if __name__ == '__main__':
    main()
