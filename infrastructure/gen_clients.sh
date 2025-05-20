#!/bin/bash
export TYPESCRIPT_POST_PROCESS_FILE="prettier --write"
openapi-generator-cli generate --enable-post-process-file -i http://rest-api:8000/openapi -g typescript-fetch -o /usr/src/app/web-app/merchant/src/rest-api --additional-properties=packageName=django_rest_api,projectName=django-rest-api,generateSourceCodeOnly=true
