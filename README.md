# Page loader
[![Maintainability](https://api.codeclimate.com/v1/badges/d800d311c65c32c837c5/maintainability)](https://codeclimate.com/github/veetors/page-loader-python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d800d311c65c32c837c5/test_coverage)](https://codeclimate.com/github/veetors/page-loader-python/test_coverage)
[![Build Status](https://travis-ci.org/veetors/page-loader.svg?branch=master)](https://travis-ci.org/veetors/page-loader)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Installation
`pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple veetors-page-loader`

## Usage
```
usage: page-loader [-h] [-O OUTPUT]
                   [--logging {debug,info,warning,error,critical}]
                   url

Download the internet page

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -O OUTPUT, --output OUTPUT
                        path to output folder (default: current working
                        directory)
  --logging {debug,info,warning,error,critical}
                        set loggin level (default: error)
```

[![example](https://asciinema.org/a/qFSqWqZkRVvIqGcLN7c1jXftH.png)](https://asciinema.org/a/qFSqWqZkRVvIqGcLN7c1jXftH)
