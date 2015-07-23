mkdir -p deploy/export


python manage.py dumpdata --indent 2 customer.interesttag> deploy/export/init_tag.json 
python manage.py dumpdata --indent 2 express.expresscarrier> deploy/export/init_express.json
