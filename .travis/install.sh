#!/usr/bin/env bash

set -e
set -x

python -m pip install tox wheel
python setup.py install