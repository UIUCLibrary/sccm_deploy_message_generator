#!/usr/bin/env bash

set -e
set -x

python -m pip install tox
python setup.py install