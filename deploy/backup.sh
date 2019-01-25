/home/git/venv/ozsales/bin/python /opt/ozsales/manage.py dumpdata --indent 4 | gzip -c > /opt/backup/ozsales/`date +%d`.json.gz
