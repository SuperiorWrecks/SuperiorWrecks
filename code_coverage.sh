#!/usr/bin/env bash
set -e  # Configure shell so that if one command fails, it exits
~/.pyenv/versions/3.6.9/bin/coverage erase
~/.pyenv/versions/3.6.9/bin/coverage run manage.py test
~/.pyenv/versions/3.6.9/bin/coverage report