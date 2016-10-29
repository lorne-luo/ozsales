env/bin/python manage.py collectstatic_js_reverse
env/bin/python manage.py collectstatic --noinput

supervisorctl restart ozsales
#supervisorctl restart celery
