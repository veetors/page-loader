# -*- coding:utf-8 -*-

import requests


def load(url):
    response = requests.get(url)

    return response.text
