#!/usr/bin/env bash

HOSTNAME=10.10.10.66
PORT=3306
USERNAME=db_user
PASSWORD=user_password
DBNAME=dbName
tableName=ngLog

basepath=$(cd `dirname $0`; pwd)
fileName=ngLogFiltered.csv
file=$basepath"/"$fileName

load_sql="LOAD DATA INFILE '"$file"' INTO TABLE "$tableName"  CHARACTER SET utf8 "
date=`date +%Y%m%d`
log=$date"-LoadData.log"
# load data to middle table from local file
# 要同时显示语句本身：-v  要增加查询结果行数：-vv  要增加执行时间：-vvv
mysql -h${HOSTNAME} -P${PORT} -u${USERNAME} -p${PASSWORD} ${DBNAME} -vvv -e  "${load_sql}" >$log