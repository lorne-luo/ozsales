mkdir -p deploy/backup
var=`date "+%Y-%m-%d-%H-%M-%S"`
mysqldump -uroot -proot ozsales > deploy/backup/ozsales_$var.sql
echo "backup current db to deploy/backup/ozsales_$var.sql"

mysqladmin drop ozsales -f -uroot -proot &&
mysqladmin create ozsales -uroot -proot &&
python manage.py syncdb --noinput &&
python manage.py migrate && 
python manage.py collectstatic --noinput &&
python manage.py collectstatic_js_reverse &&
python manage.py init_groups &&
python manage.py loaddata deploy/backup.json

#python manage.py createsuperuser