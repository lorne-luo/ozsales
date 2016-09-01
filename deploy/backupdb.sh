DATE=`date +%F`
mysqldump -uroot -proot ozsales > ozsales-${DATE}.sql
