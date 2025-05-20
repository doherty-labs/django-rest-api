#!/bin/bash
set -e
if [[ "$APP_ENV" == "test" ]]; then
   op inject -i /usr/src/app/web-app/env.test.tmpl -o /usr/src/app/web-app/.env.production --force
elif [[ "$APP_ENV" == "production" ]]; then
   op inject -i /usr/src/app/web-app/env.production.tmpl -o /usr/src/app/web-app/.env.production --force
elif [[ "$APP_ENV" == "development" ]]; then
   op inject -i /usr/src/app/web-app/env.development.tmpl -o /usr/src/app/web-app/.env.development --force
else
   echo "Secrets injection is not supported in this environment"
   echo "Please set APP_ENV to test, production, or development"
fi
