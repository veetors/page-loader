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


def get_assets(doc):
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

    return assets


def download_asset(url, path, output_path):
    response = requests.get(url + path)

    filename = get_filename_from_path(path)

    with open(os.path.join(output_path, filename), 'w') as output_file:
        output_file.write(response.text)


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

    main_file_name = get_filename_from_url(url)

    with open(os.path.join(output_path, main_file_name), 'w') as output_file:
        output_file.write(response.text)

    assets = get_assets(response.text)
    print('assets', assets)

    if not assets:
        return

    assets_dir_path = os.path.join(output_path, get_dirname(url))

    print('assets_dir_path', assets_dir_path)

    os.mkdir(assets_dir_path)

    for asset in assets:
        download_asset(
            url=urlparse(url).scheme + '://' + urlparse(url).netloc,
            path=asset,
            output_path=assets_dir_path,
        )
