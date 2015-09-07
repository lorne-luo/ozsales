killall -2 -I uwsgi
python manage.py collectstatic --noinput
sudo -u luotao uwsgi --ini settings/uwsgi.ini
#echo "/usr/bin/uwsgi --ini /data/django/ozsales/settings/uwsgi.ini"|su - uwsgi

#supervisorctl update
#supervisorctl start ozsales
#uwsgi --chdir=/data/django/ozsales --module=settings.wsgi:application --env DJANGO_SETTINGS_MODULE=settings.settings --master --pidfile=/tmp/uwsgi-ozsales.pid --socket=/tmp/uwsgi.sock --processes=1 --harakiri=20 --max-requests=500 --vacuum --strict --chmod-socket=666
