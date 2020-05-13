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
    with open(get_fixtures_path('without_assets_before.html')) as mock_file:
        mock_content = mock_file.read()
    requests_mock.get(TEST_URL, text=mock_content)

    with open(get_fixtures_path('without_assets_after.html')) as expected_file:
        expected = expected_file.read()

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, TEST_FILENAME)) as acctual_file:
            acctual = acctual_file.read()

    assert acctual == expected


def test_main_with_assets(requests_mock):  # noqa: D103
    with open(get_fixtures_path('with_assets_before.html')) as mock_file:
        mock_content = mock_file.read()

    requests_mock.get(TEST_URL, text=mock_content)
    requests_mock.get('https://hexlet.io/assets/application.js')
    requests_mock.get('https://hexlet.io/assets/application.css')
    requests_mock.get('https://hexlet.io/assets/image.jpg')

    with open(
        get_fixtures_path('with_assets_after.html'),
    ) as expected_html_file:
        expected_html = expected_html_file.read()

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, TEST_FILENAME)) as acctual_file:
            acctual_main_content = acctual_file.read()

        assert acctual_main_content == expected_html
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses_files', 'assets-application.js',
        ))
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses_files', 'assets-application.css',
        ))
        assert os.path.exists(os.path.join(
            tmpdirname, 'hexlet-io-courses_files', 'assets-image.jpg',
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
