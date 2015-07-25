killall -2 -I uwsgi
python manage.py collectstatic
uwsgi --ini settings/uwsgi.ini
