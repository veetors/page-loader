# -*- coding:utf-8 -*-

"""Errors module."""


class NetworkError(Exception):  # noqa: D101
    code = 1


class StorageError(Exception):  # noqa: D101
    code = 2
