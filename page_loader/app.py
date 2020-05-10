# -*- coding:utf-8 -*-

import os

import requests


def load(url, output_path=os.getcwd()):
    response = requests.get(url)

    with open(os.path.join(output_path, 'test.html'), 'w') as output_file:
        output_file.write(response.text)
