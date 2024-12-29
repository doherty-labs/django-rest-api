#!/bin/bash


# pip install openapi-generator-cli[jdk4py]

export PYTHON_POST_PROCESS_FILE="./format_file.sh"
export TYPESCRIPT_POST_PROCESS_FILE="prettier --write"

openapi-generator-cli generate --enable-post-process-file -i http://rest-api:8000/openapi -g python-pydantic-v1 -o /usr/src/app/api/clients/python --additional-properties=packageName=django_rest_api,projectName=django-rest-api,generateSourceCodeOnly=true
openapi-generator-cli generate --enable-post-process-file -i http://rest-api:8000/openapi -g typescript-fetch -o /usr/src/app/api/clients/typescript --additional-properties=packageName=django_rest_api,projectName=django-rest-api,generateSourceCodeOnly=true