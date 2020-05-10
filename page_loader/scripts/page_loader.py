#!/usr/bin/env python3
# -*- coding:utf-8 -*

"""Package entry point."""

import page_loader


def main():
    """Run main function."""
    output = page_loader.load('https://hexlet.io/courses')

    print(output)


if __name__ == '__main__':
    main()
