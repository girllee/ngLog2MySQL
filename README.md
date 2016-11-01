Nginx log analysis
==================
 A simple implement of nginx log data to mysql.
 -----------------
 使用方法:
 1. 初始化数据库,选择一个数据库,在其中执行ngLog.sql
 2. 将ng日志放于当前目录下,执行NgLogAnalysis.py,执行成功后会生成ngLogFiltered.csv文件
 3. vi loadData.sh 修改其中的数据库连接配置后执行.
 4. 可以设置定时任务每天定时执行