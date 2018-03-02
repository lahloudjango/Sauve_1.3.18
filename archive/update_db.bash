#!/bin/bash

mysql --host=localhost --port=3306 --user=root --password=rootmysql --protocol=TCP < update_db.sql

python manage.py syncdb

#python manage.py loaddata 2015-09-22.json


