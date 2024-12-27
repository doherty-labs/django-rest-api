#!/bin/bash
ruff check --fix $1
flake8 $1
isort $1 --profile black
black $1