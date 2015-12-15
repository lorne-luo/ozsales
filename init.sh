mkdir -p deploy/backup
var=`date "+%Y-%m-%d-%H-%M-%S"`
mysqldump -uroot -proot ozsales > deploy/backup/ozsales_$var.sql
echo "backup current db to deploy/backup/ozsales_$var.sql"

mysqladmin drop ozsales -f -uroot -proot &&
mysqladmin create ozsales -uroot -proot &&
python manage.py makemigrations && 
python manage.py syncdb --noinput && 
python manage.py migrate && 
python manage.py init_groups &&
python manage.py init_data &&
python manage.py collectstatic --noinput &&
python manage.py collectstatic_js_reverse &&
python manage.py loaddata deploy/init_user.json &&
python manage.py loaddata deploy/init_product.json &&
python manage.py loaddata deploy/init_tag.json &&
python manage.py loaddata deploy/init_express.json

# for test
#python manage.py loaddata deploy/test_data.json
#python manage.py createsuperuser