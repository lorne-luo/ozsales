# mysqldump -uroot -plt1116 ozsales | gzip -c > /home/luotao/backup/ozsales/`date +%d`.sql.gz

sudo -u postgres pg_dump youdan | gzip -c > /opt/backup/ozsales/`date +%d`.sql.gz
