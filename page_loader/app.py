# -*- coding:utf-8 -*-

"""Module with functions for load page."""

import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

REGEXP = '[^0-9a-zA-Z]+'


def get_filename_from_url(url):  # noqa: D103
    parsed_url = urlparse(url)

    return '{0}.html'.format(
        re.sub(REGEXP, '-', parsed_url.netloc + parsed_url.path),
    )


def get_filename_from_path(path):  # noqa: D103
    filepath, extansion = os.path.splitext(path)
    formated_path = re.sub(REGEXP, '-', filepath[1:])

    return formated_path + extansion


def get_dirname(url):  # noqa: D103
    parsed_url = urlparse(url)

    return '{0}_files'.format(
        re.sub(REGEXP, '-', parsed_url.netloc + parsed_url.path),
    )


def parse_doc(doc):
    soup = BeautifulSoup(doc, 'html.parser')

    assets = []
    tags = [*soup('script'), *soup('link'), *soup('img')]

    for tag in tags:
        url_attr = 'href' if tag.name == 'link' else 'src'
        url = tag.get(url_attr)

        if not url:
            continue

        if not urlparse(url).netloc:
            assets.append(url)

    print(assets)


def load(url, output_path=None):
    """Load the page at the appropriate url and write to a file.

    Args:
        url (str): target url
        output_path (str): path for output file

    Raises:
        ValueError: page not found
    """
    if not output_path:
        output_path = os.getcwd()

    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError('Page not found.')

    parse_doc(response.text)

    filename = get_filename_from_url(url)

    with open(os.path.join(output_path, filename), 'w') as output_file:
        output_file.write(response.text)
