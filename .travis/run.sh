#!/usr/bin/env bash

set -e
set -x

tox -e $(echo py$TRAVIS_PYTHON_VERSION | tr -d .)
deploymessage --pytest
python setup.py sdist