# -*- coding:utf-8 -*-

"""Filename generation tests."""

from page_loader.lib.page import format_asset_name, format_name

URL = 'https://hexlet.io/courses'
JS_PATH = '/assets/application.js'
CSS_PATH = '/assets/application.css'
IMG_PATH = '/assets/image.jpg'
EXPECTED_HTML_NAME = 'hexlet-io-courses.html'
EXPECTED_ASSET_FOLDER_NAME = 'hexlet-io-courses_files'
EXPECTED_JS_NAME = 'assets-application.js'
EXPECTED_CSS_NAME = 'assets-application.css'
EXPECTED_IMG_NAME = 'assets-image.jpg'


def test_filename_form_url():
    assert format_name(URL) == EXPECTED_HTML_NAME


def test_dirname():
    assert format_name(URL, directory=True) == EXPECTED_ASSET_FOLDER_NAME


def test_filename_from_path():
    assert format_asset_name(JS_PATH) == EXPECTED_JS_NAME
    assert format_asset_name(CSS_PATH) == EXPECTED_CSS_NAME
    assert format_asset_name(IMG_PATH) == EXPECTED_IMG_NAME
