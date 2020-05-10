#!/usr/bin/env python3
# -*- coding:utf-8 -*

import page_loader

def main():
    print('Welcon to Page Loader.')

    output = page_loader.load('https://hexlet.io/courses')

    print(output)


if __name__ == '__main__':
    main()
