env/bin/python manage.py collectstatic_js_reverse
cp -rf collectstatic/django_js_reverse/js/reverse.js static/django_js_reverse/js/reverse.js

env/bin/python manage.py collectstatic --noinput
supervisorctl restart ozsales
supervisorctl restart celery
