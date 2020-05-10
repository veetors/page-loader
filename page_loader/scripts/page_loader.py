#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import argparse

import page_loader


def main():
    """Run main function."""
    parser = argparse.ArgumentParser(description='Download the internet page')
    parser.add_argument('url')
    parser.add_argument(
        '-O',
        '--output',
        type=str,
        help='path to output folder (default: current working directory)',
    )
    args = parser.parse_args()

    page_loader.load(args.url, args.output)


if __name__ == '__main__':
    main()
