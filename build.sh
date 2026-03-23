#!/usr/bin/env bash

set -o errexit

if [ -f requirements-render.txt ]; then
  pip install -r requirements-render.txt
else
  pip install -r requirements.txt
fi

python manage.py collectstatic --noinput
python manage.py migrate
