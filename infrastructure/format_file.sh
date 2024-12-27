#!/bin/bash
ruff check --fix --unsafe-fixes $1
flake8 $1
isort $1 --profile black
black $1