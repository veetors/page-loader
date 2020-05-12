#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import argparse
import sys

import requests

import page_loader


def get_parser():  # noqa: D103
    parser = argparse.ArgumentParser(description='Download the internet page')
    parser.add_argument('url')
    parser.add_argument(
        '-O',
        '--output',
        type=str,
        help='path to output folder (default: current working directory)',
    )
    return parser


def main():
    """Run main function."""  # noqa: DAR401
    parser = get_parser()
    args = parser.parse_args()

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
