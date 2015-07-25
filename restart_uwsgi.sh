killall -2 -I uwsgi
python manage.py collectstatic --noinput
uwsgi --ini settings/uwsgi.ini
