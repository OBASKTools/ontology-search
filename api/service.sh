#!/bin/bash

[[ -z "$SOLR_HOST" ]] && echo "ERROR: SOLR_HOST must be set" && exit 1
[[ -z "$SOLR_PORT" ]] && echo "ERROR: SOLR_PORT must be set" && exit 1
[[ -z "$SOLR_COLLECTION" ]] && echo "ERROR: SOLR_COLLECTION must be set" && exit 1

[[ -z "$WEB_EXPOSE_HOSTNAME" ]] && echo "ERROR: WEB_EXPOSE_HOSTNAME must be set" && exit 1
[[ -z "$WEB_EXPOSE_PORT" ]] && echo "ERROR: WEB_EXPOSE_PORT must be set" && exit 1

export APP_HOME=/app

export PYTHON_ENV=production

source /venv/bin/activate

python3 -u $APP_HOME/src/app.py
