# -*- coding:utf-8 -*-

"""Filename generation tests."""

from page_loader.app import (
    get_dirname,
    get_filename_from_path,
    get_filename_from_url,
)

URL = 'https://hexlet.io/courses'
JS_PATH = '/assets/application.js'
CSS_PATH = '/assets/application.css'
IMG_PATH = '/assets/image.jpg'


def test_filename_form_url():  # noqa: D103
    expected = 'hexlet-io-courses.html'
    acctual = get_filename_from_url(URL)
    assert acctual == expected


def test_filename_from_path():  # noqa: D103
    expected_js = 'assets-application.js'
    expected_css = 'assets-application.css'
    expected_img = 'assets-image.jpg'

    assert get_filename_from_path(JS_PATH) == expected_js
    assert get_filename_from_path(CSS_PATH) == expected_css
    assert get_filename_from_path(IMG_PATH) == expected_img


def test_dirname():   # noqa: D103
    expected = 'hexlet-io-courses_files'
    acctual = get_dirname(URL)
    assert acctual == expected
