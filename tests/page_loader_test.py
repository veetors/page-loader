# -*- coding:utf-8 -*-

"""Page-loader tests."""

import os
import tempfile

import page_loader

TEST_URL = 'https://hexlet.io/courses'
TEST_FILENAME = 'hexlet-io-courses.html'


def get_fixtures_path(filename):
    return os.path.join(os.getcwd(), 'tests', 'fixtures', filename)


def test_page_loader(requests_mock):
    with open(get_fixtures_path('expected.html')) as expected_file:
        expected = expected_file.read()

    requests_mock.get(TEST_URL, text=expected)

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_loader.load(TEST_URL, tmpdirname)

        with open(os.path.join(tmpdirname, TEST_FILENAME)) as acctual_file:
            acctual = acctual_file.read()

    assert acctual == expected
