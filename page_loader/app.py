# -*- coding:utf-8 -*-

"""Module with functions for load page."""

import logging
import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

REGEXP = '[^0-9a-zA-Z]+'
URL = 'url'
FILENAME = 'filename'
OUTPUT_PATH = 'output_path'


def format_name(url, directory=False):  # noqa: D103
    parsed_url = urlparse(url)
    base = re.sub(REGEXP, '-', parsed_url.netloc + parsed_url.path)
    suffix = '_files' if directory else '.html'

    return base + suffix


def format_asset_name(path):  # noqa: D103
    filepath, extansion = os.path.splitext(path)
    formated_path = re.sub(REGEXP, '-', filepath[1:])

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
        assets.append({
            URL: full_asset_url,
            FILENAME: format_asset_name(asset_url),
        })
        tag[current_attr] = '{0}/{1}'.format(
            format_name(url, directory=True),
            format_asset_name(asset_url),
        )

    return (page.prettify(formatter='html5'), assets)


def download_asset(asset):  # noqa: D103
    response = requests.get(asset[URL], stream=True)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as request_e:
        logging.error('Download resource error. {0}'.format(str(request_e)))
        return

    with open(
        os.path.join(asset[OUTPUT_PATH], asset[FILENAME]), 'wb',
    ) as output_file:
        for chunk in response:
            output_file.write(chunk)


def download_assets(assets, output_path):  # noqa: D103
    os.mkdir(output_path)

    assets_with_path = map(
        lambda asset: {**asset, OUTPUT_PATH: output_path},
        assets,
    )

    with ThreadPool(8) as pool:
        pool.map(download_asset, assets_with_path)


def load(url, output_path=None):  # noqa: WPS210
    """Load the page at the appropriate url and write to a file.

    Args:
        url (str): target url
        output_path (str): path for output file
    """
    if not output_path:
        output_path = os.getcwd()

    response = requests.get(url)
    response.raise_for_status()

    html_file_name = format_name(url)
    html, assets = format_html(response.text, url)
    with open(os.path.join(output_path, html_file_name), 'w') as html_file:
        html_file.write(html)

    if not assets:
        return

    assets_dir_path = os.path.join(
        output_path, format_name(url, directory=True),
    )
    download_assets(assets, assets_dir_path)
