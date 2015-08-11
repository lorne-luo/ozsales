killall -2 -I uwsgi
python manage.py collectstatic --noinput
sudo -u luotao uwsgi --ini settings/uwsgi.ini
#echo "/usr/bin/uwsgi --ini /data/django/ozsales/settings/uwsgi.ini"|su - uwsgi

#supervisorctl update
#supervisorctl start ozsales
