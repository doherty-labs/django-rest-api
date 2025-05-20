#!/bin/bash
set -e

if [[ "$APP_ENV" == "development" ]]; then
   op inject -i /usr/src/app/web-app/env.development.tmpl -o /usr/src/app/web-app/.env.development --force
   exec npm run dev
fi

exec npm start