# -*- coding:utf-8 -*-

import os

import page_loader

TEST_URL = 'https://test-url.com'


def get_fixtures_path(filename):
    return os.path.join(os.getcwd(), 'tests', 'fixtures', filename)


def test_page_loader(requests_mock):
    with open(get_fixtures_path('expected.html')) as expected_file:
        expected = expected_file.read()

    requests_mock.get(TEST_URL, text=expected)

    acctual = page_loader.load(TEST_URL)

    assert acctual == expected
