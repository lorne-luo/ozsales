#!/bin/bash
set -e

PROJECT_ROOT=/opt/django/ozsales
PILOT_PYTHON=$PROJECT_ROOT/env/bin/python

git --git-dir=$PROJECT_ROOT/.git/ pull

$PILOT_PYTHON $PROJECT_ROOT/manage.py collectstatic_js_reverse
$PILOT_PYTHON $PROJECT_ROOT/manage.py collectstatic --noinput

COMMIT_INFO=`git --git-dir=$PROJECT_ROOT/.git/ show -s --date=iso8601 --format='{"commit": "%h", "date": "%ad", "comment": "%s"}'`
echo [`date +%Y-%m-%d\ %H:%M:%S`] $COMMIT_INFO >> $PROJECT_ROOT/media/upgrade.txt

exec "$@"
