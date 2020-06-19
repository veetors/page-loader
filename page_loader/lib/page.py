# -*- coding:utf-8 -*-

"""Module with functions for load page."""

import logging
import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.lib.errors import NetworkError, StorageError

ALPHANUM = re.compile(r'[^0-9a-zA-Z]+')
URL = 'url'
FILENAME = 'filename'


def format_name(url, directory=False):  # noqa: D103
    parsed_url = urlparse(url)
    base = re.sub(ALPHANUM, '-', parsed_url.netloc + parsed_url.path)
    suffix = '_files' if directory else '.html'

    return base + suffix


def format_asset_name(path):  # noqa: D103
    filepath, extansion = os.path.splitext(path)
    formated_path = re.sub(ALPHANUM, '-', filepath[1:])

    return formated_path + extansion


def format_html(html, url):  # noqa: WPS210, D103
    page = BeautifulSoup(html, 'html.parser')
    scheme, netloc, *_ = urlparse(url)

    assets = []
    tags = [*page('script'), *page('link'), *page('img')]  # noqa: WPS221

    for tag in tags:
        current_attr = 'href' if tag.name == 'link' else 'src'
        asset_url = tag.get(current_attr)

        if not asset_url or urlparse(asset_url).netloc:
            continue

        full_asset_url = '{0}://{1}{2}'.format(scheme, netloc, asset_url)
        assets.append((full_asset_url, format_asset_name(asset_url)))
        tag[current_attr] = '{0}/{1}'.format(
            format_name(url, directory=True),
            format_asset_name(asset_url),
        )

    return (page.prettify(formatter='html5'), assets)


def download_assets(assets, output_path):  # noqa: D103, WPS210
    os.mkdir(output_path)

    for url, filename in assets:
        response = requests.get(url, stream=True)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as request_e:
            logging.error('Download resource error. {0}'.format(str(request_e)))
            continue

        with open(
            os.path.join(output_path, filename), 'wb',
        ) as output_file:
            content_length = int(response.headers.get('content-length', '0'))
            chunk_size = 128
            quantity_of_chunks = (content_length / chunk_size) + 1
            with Bar(filename, max=quantity_of_chunks) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    output_file.write(chunk)
                    progress_bar.next()  # noqa: B305


def download(url, output_path=None):  # noqa: C901, WPS210
    """Load the page at the appropriate url and write to a file.

    Args:
        url (str): target url
        output_path (str): path for output file

    Raises:
        NetworkError: network error
        StorageError: storage error
    """
    if not output_path:
        output_path = os.getcwd()

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as request_e:
        raise NetworkError('Network error.') from request_e

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_e:
        raise NetworkError('Network error.') from http_e

    html_file_name = format_name(url)
    html, assets = format_html(response.text, url)

    try:
        with open(os.path.join(output_path, html_file_name), 'w') as html_file:
            html_file.write(html)
    except (FileNotFoundError, PermissionError) as storage_e:
        raise StorageError('Storage error.') from storage_e

    if not assets:
        return

    assets_dir_path = os.path.join(
        output_path, format_name(url, directory=True),
    )

    download_assets(assets, assets_dir_path)
