mysqladmin drop ozsales -f -uroot -proot &&
mysqladmin create ozsales -uroot -proot &&
python manage.py makemigrations && 
python manage.py syncdb --noinput && 
python manage.py migrate && 
python manage.py init_groups && 
python manage.py init_data &&
python manage.py loaddata deploy/init_product.json

#python manage.py loaddata deploy/auth.json &&
#python manage.py loaddata deploy/test_data.json
#python manage.py collectstatic
# && python manage.py createsuperuser
