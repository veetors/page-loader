# -*- coding:utf-8 -*-

"""Page-loader tests."""

import os
import tempfile

import pytest

import page_loader

TEST_URL = 'https://hexlet.io/courses'
TEST_FILENAME = 'hexlet-io-courses.html'


def get_fixtures_path(filename):  # noqa: D103
    return os.path.join(os.getcwd(), 'tests', 'fixtures', filename)


def test_main_without_assets(requests_mock):  # noqa: D103
    with open(get_fixtures_path('without_assets.html')) as expected_file:
        expected = expected_file.read()

    requests_mock.get(TEST_URL, text=expected)

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, TEST_FILENAME)) as acctual_file:
            acctual = acctual_file.read()

    assert acctual == expected


def test_main_with_assets(requests_mock):  # noqa: D103
    with open(get_fixtures_path('with_assets.html')) as expected_file:
        expected_main_content = expected_file.read()

    requests_mock.get(TEST_URL, text=expected_main_content)
    requests_mock.get('https://hexlet.io/assets/application.js')
    requests_mock.get('https://hexlet.io/assets/application.css')
    requests_mock.get('https://hexlet.io/assets/image.jpg')

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, TEST_FILENAME)) as acctual_file:
            acctual_main_content = acctual_file.read()

        assert acctual_main_content == expected_main_content
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses', 'assets-application.js',
        ))
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses', 'assets-application.css',
        ))
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses', 'assets-image.jpg',
        ))


def test_page_not_found(requests_mock):  # noqa: D103
    requests_mock.get(TEST_URL, status_code=404)

    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(ValueError) as wrapped_e:
            page_loader.load(TEST_URL, tmpdirname)
        assert str(wrapped_e.value) == 'Page not found.'  # noqa: WPS441


def test_wrong_output_path(requests_mock):  # noqa: D103
    requests_mock.get(TEST_URL)

    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(FileNotFoundError):
            assert page_loader.load(
                TEST_URL,
                os.path.join(tmpdirname, 'wrong_path'),
            )
