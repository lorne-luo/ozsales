/opt/django/ozsales/env/bin/python /opt/django/ozsales/manage.py dumpdata --indent 4 | gzip -c > /home/luotao/backup/ozsales/`date +%d`.json.gz
