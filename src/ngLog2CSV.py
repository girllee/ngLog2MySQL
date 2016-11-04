#!/usr/bin/env python
# coding:utf8
import time
import re

__author__ = 'Asin Liu'

"""
分析导流页面的请求数据,生成可以导入到SQL中的.csv格式的文档,后续的处理可以是使用
MySQL的LoadData 功能将数据导入到指定的数据库表中.

如有问题请给我发邮件:　dozray@163.com
"""

date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

logPath = '/usr/local/nginx/logs/'
logFile = logPath + 'access_' + date + '-00.log'

logFile = '/home/boot/vmShare/ngLog/acc.log'

'''
Ｎginx 日志的默认的
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"'

有两种解决此问题的方法:
1.将行记录分为前后两个部分,前半部分使用分隔(split方式性能较好),后半部分使用正则表达式.
2.全部使用正则表式
'''

# -------------------------------------------------------
# 正则表达式
# -------------------------------------------------------
# 111.73.174.192 - - [23/Dec/2015:11:48:01 +0800] "GET /static/images/header/snow.png HTTP/1.1" 304 0 "http://www.heyunchou.com/event/anniversaryBak.jsp?tg_src=b94cdbe2901343139d8494c2bc8769d5" "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/5.0)"

re_ip = r"?P<ip>[\d.]*"
re_time = r"""?P<time>\[[^\[\]]*\]"""
re_request = r"""?P<request>\"[^\"]*\""""
re_status = r"?P<status>\d+"
re_bytes = r"?P<bodyByte>\d+"
re_referrer = r"""?P<referrer>\"[^\"]*\""""
re_ua = r"""?P<ua>\"[^\"]*\""""

re_ub = re.compile(r'[^)]*\"')
re_us = re.compile(r'\([^()]*\)')
re_ngLog = re.compile(r"(%s)\ -\ -\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)"
                      % (re_ip, re_time, re_request, re_status, re_bytes, re_referrer, re_ua), re.VERBOSE)

out = open(r'ngLogFiltered.csv', 'wb')

excludesStart = ["/hyc-app/api", "/wap/common/images", "/upload", "/static"]
excludesEnd = ["ico", "gif", "jpg", "png", "css", "do", "js", "inc", "json", "xml"]
with open(logFile, 'r') as f:
    while True:
        try:
            line = f.readline()
            if not line:
                break
            sp = line.split()
            url = sp[6]
            found = False
            for k, v in enumerate(excludesStart):
                if url.startswith(v):
                    found = True
                    break
            if found:
                continue

            for k, v in enumerate(excludesEnd):
                if url.endswith(v):
                    found = True
                    break
            if found:
                continue

            print(line)

            match = re_ngLog.match(line)  # if match is not None:
            if match is not None:
                grps = match.groups()
                ip = grps[0]
                reqTime = grps[1]
                request = grps[2]
                status = grps[3]
                bodyBytes = grps[4]
                referrer = grps[5]
                userAgent = grps[6]
                # format the date
                reqTime = reqTime[1:-7]
                t = time.strptime(reqTime, "%d/%b/%Y:%H:%M:%S")
                reqTime = time.strftime("%Y-%m-%d %X", t)

                # get rid of " "
                request = request[1: -1]
                req = request.split(" ")
                method = req[0]
                if len(req) > 1:
                    uri = req[1]

                referrer = referrer[1:-1]
                # userAgent = userAgent[1:-1]

                if len(userAgent) > 20:
                    userInfo = userAgent.split(' ')
                    userKernel = userInfo[0]
                    try:
                        userSystem = re_us.findall(userAgent)
                        userSystem = userSystem[0]
                        userSystem = userSystem[1:-1]
                        # print(userSystem)
                        ub = re_ub.findall(userAgent)
                        ub = ub[1]
                        userBrowser = ub.replace('"', '')

                        lst = [reqTime, ip, method, uri, status, bodyBytes, referrer, userAgent, userSystem,
                               userBrowser]
                    except IndexError:
                        lst = [reqTime, ip, method, uri, status, bodyBytes, referrer, userAgent, "", ""]

                else:
                    lst = [reqTime, ip, method, uri, status, bodyBytes, referrer, userAgent, "", ""]

                line = ''.join((e + '\t') for e in lst)
                line = line + '\n'
                out.writelines(line)
        finally:
            pass
out.close()
