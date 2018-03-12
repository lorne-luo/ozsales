#!/bin/bash
##################
# Simple deploy script
##################

WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )" &&
cd $WORKDIR &&
PULL_INFO=$(git pull 2>/dev/null)

if [ "$PULL_INFO" == "Already up-to-date." ]; then
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

touch $WORKDIR/media/upgrade.txt
sed  -i '1i ['"`date +%Y-%m-%d\ %H:%M:%S`"'] '"$COMMIT_INFO" $WORKDIR/media/upgrade.txt
exec "$@"
