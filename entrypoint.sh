#!/bin/bash

. venv/bin/activate

exec gunicorn --bind 0.0.0.0:3035 --workers 3 --timeout 0 config.wsgi:application
