# -*- coding:utf-8 -*-

"""Page-loader tests."""

import os
import tempfile

import pytest

import page_loader

page_loader.logger.init()

TEST_URL = 'https://hexlet.io/courses'
HTML_FILENAME = 'hexlet-io-courses.html'
ASSETS_DIRNAME = 'hexlet-io-courses_files'
URL = 'url'
NAME_BEFORE = 'name_before'
NAME_AFTER = 'name_after'
RB = 'rb'
ASSETS = (
    {
        URL: 'https://hexlet.io/assets/application1.js',
        NAME_BEFORE: 'application1.js',
        NAME_AFTER: 'assets-application1.js',
    },
    {
        URL: 'https://hexlet.io/assets/application2.js',
        NAME_BEFORE: 'application2.js',
        NAME_AFTER: 'assets-application2.js',
    },
    {
        URL: 'https://hexlet.io/assets/application1.css',
        NAME_BEFORE: 'application1.css',
        NAME_AFTER: 'assets-application1.css',
    },
    {
        URL: 'https://hexlet.io/assets/application2.css',
        NAME_BEFORE: 'application2.css',
        NAME_AFTER: 'assets-application2.css',
    },
    {
        URL: 'https://hexlet.io/assets/image1.png',
        NAME_BEFORE: 'image1.png',
        NAME_AFTER: 'assets-image1.png',
    },
    {
        URL: 'https://hexlet.io/assets/image2.jpg',
        NAME_BEFORE: 'image2.jpg',
        NAME_AFTER: 'assets-image2.jpg',
    },
)


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

        with open(os.path.join(tmpdirname, HTML_FILENAME)) as acctual_file:
            acctual = acctual_file.read()

    assert acctual == expected


@pytest.mark.parametrize('asset', ASSETS)
def test_main_with_assets(requests_mock, asset):  # noqa: D103
    with open(get_fixtures_path('with_assets_before.html')) as mock_html_file:
        mock_html_content = mock_html_file.read()
    requests_mock.get(TEST_URL, text=mock_html_content)
    for mock_asset in ASSETS:
        with open(
            get_fixtures_path(mock_asset[NAME_BEFORE]), RB,
        ) as mock_asset_file:
            mock_asset_content = mock_asset_file.read()
        requests_mock.get(mock_asset[URL], content=mock_asset_content)

    with open(
        get_fixtures_path('with_assets_after.html'),
    ) as expected_html_file:
        expected_html_content = expected_html_file.read()
    with open(
        get_fixtures_path(asset[NAME_BEFORE]), RB,
    ) as expected_asset_file:
        expected_asset_content = expected_asset_file.read()

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, HTML_FILENAME)) as acctual_html_file:
            acctual_html_content = acctual_html_file.read()
        with open(
            os.path.join(tmpdirname, ASSETS_DIRNAME, asset[NAME_AFTER]), RB,
        ) as acctual_asset_file:
            acctual_asset_content = acctual_asset_file.read()

        assert acctual_html_content == expected_html_content
        assert acctual_asset_content == expected_asset_content


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
