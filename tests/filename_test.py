# -*- coding:utf-8 -*-

"""Filename generation tests."""

from page_loader.app import format_name, format_asset_name

URL = 'https://hexlet.io/courses'
JS_PATH = '/assets/application.js'
CSS_PATH = '/assets/application.css'
IMG_PATH = '/assets/image.jpg'


def test_filename_from_path():  # noqa: D103
    expected_js = 'assets-application.js'
    expected_css = 'assets-application.css'
    expected_img = 'assets-image.jpg'

    assert format_asset_name(JS_PATH) == expected_js
    assert format_asset_name(CSS_PATH) == expected_css
    assert format_asset_name(IMG_PATH) == expected_img


def test_filename_form_url():  # noqa: D103
    expected = 'hexlet-io-courses.html'
    acctual = format_name(URL)
    assert acctual == expected


def test_dirname():   # noqa: D103
    expected = 'hexlet-io-courses_files'
    acctual = format_name(URL, directory=True)
    assert acctual == expected
