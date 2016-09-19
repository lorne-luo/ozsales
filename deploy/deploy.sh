#!/bin/bash
##################
# Simple deploy script
##################

WORKDIR=/data/django/ozsales/
cd $WORKDIR

updated=$(git pull 2>/dev/null)
if [ "$updated" == 'Already up-to-date.' ]; then
    # Nothing to do, exit cleanly
    #exit 0
    COMMIT_INFO=No\ updates,\ restart.
else
    # Code has been updated, rebuild the app

    PILOT_PYTHON=$WORKDIR/env/bin/python
    $PILOT_PYTHON manage.py migrate
    $PILOT_PYTHON manage.py collectstatic_js_reverse
    $PILOT_PYTHON manage.py collectstatic --noinput
    COMMIT_INFO=`git show -s --date=iso8601 --format='{"commit": "%h", "date": "%ad", "comment": "%s"}'`

    # And eventually restart the app
    #supervisorctl restart ozsales
fi

echo [`date +%Y-%m-%d\ %H:%M:%S`] $COMMIT_INFO >> $WORKDIR/media/upgrade.txt
exec "$@"
