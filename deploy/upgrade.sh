#!/bin/bash
set -e

PROJECT_ROOT=/data/django/ozsales
PILOT_PYTHON=$PROJECT_ROOT/env/bin/python

git --git-dir=$PROJECT_ROOT/.git/ pull

$PILOT_PYTHON $PROJECT_ROOT/manage.py collectstatic_js_reverse
$PILOT_PYTHON $PROJECT_ROOT/manage.py collectstatic --noinput

exec "$@"
