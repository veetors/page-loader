#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import logging
import sys

from page_loader.lib import args_parser, log_level, page
from page_loader.lib.errors import NetworkError, StorageError


def main():  # noqa: WPS213
    """Run main function."""
    parser = args_parser.get()
    args = parser.parse_args()

    logging.basicConfig(
        format='%(levelname)s:%(message)s',  # noqa: WPS323
        level=log_level.get(args.logging),
    )

    logging.debug(args.url)
    logging.debug(args.output)

    try:
        page.download(args.url, args.output)
    except (NetworkError, StorageError) as wrapped_e:
        logging.error(str(wrapped_e))
        logging.debug(str(wrapped_e.__cause__))  # noqa: WPS609
        sys.exit(wrapped_e.code)


if __name__ == '__main__':
    main()
