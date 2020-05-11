# -*- coding:utf-8 -*-

"""Module with functions for load page."""

import os
import re
from urllib.parse import urlparse

import requests


def get_filename(url):  # noqa: D103
    parsed_url = urlparse(url)

    return '{0}.html'.format(
        re.sub('[^0-9a-zA-Z]+', '-', parsed_url.netloc + parsed_url.path),
    )


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

    filename = get_filename(url)

    with open(os.path.join(output_path, filename), 'w') as output_file:
        output_file.write(response.text)
