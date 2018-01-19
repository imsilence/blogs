title: logging模块
date: 2015-05-27 23:18:21
tags: [python, logging]
categories: [python]
---

## 简介 ##

logging模块是python日志管理模块

## 使用 ##

```
In [19]: import logging

In [20]: logging.critical('this is critical msg')
CRITICAL:root:this is critical msg

In [21]: logging.error('this is error msg')
ERROR:root:this is error msg

In [22]: logging.warning('this is warning msg')
WARNING:root:this is warning msg

In [23]: logging.info('this is info msg')

In [24]: logging.debug('this is debug msg')
```

日志级别：

`CRITICAL > ERROR > WARNING(默认) > INFO > DEBUG > NOTSET`

默认日志格式:

`LOGLEVEL:LOGGERNAME:msg`

## 日志级别，日志格式，输出位置设置 ##

使用logging.basicConfig进行日志输出信息配置

```
logging.basicConfig(level=logging.DEBUG,
                    format='',
                    datefmt='',
                    filemode='',
                    filename=''
)
```

参数说明:

1.level:指定日志记录级别,可选值logging.ERROR/WARNING/INFO/DEBUG
2.format:指定日志输出格式：

|参数|说明|
|-----|-----|
|%(name)s|Logger的名字|
|%(levelno)s|数字日志级别|
|%(levelname)s|文本日志级别|
|%(pathname)s|调用日志输出函数的模块文件路径|
|%(filenames)s|调用日志输出函数的模块文件名|
|%(module)s|调用日志输出函数的模块名|
|%(funcName)s|调用日志输出函数的函数名|
|%(lineno)d|调用日志输出函数语句所在行号|
|%(created)f|当前时间|
|%(relativeCreated)d|当前时间|
|%(asctime)s|当前时间,格式'2015-05-28 20:50:03,345'|
|%(thread)d|线程id|
|%(threadName)s|线程名|
|%(process)d|进程id|
|%（message)s|消息|

3.datefmt:指定日志中日期格式
4.filemode:指定文件打开方式
5.filename:指定日志文件位置
6.stream:制定stream创建StreamHandler,若同时存在filename和stream时，filename启用

## logging.getLogger() ##

```
import logging

logger = logging.getLogger()

mlogger = logging.getLogger('com.uk.silence')
mlogger.setLevel(logging.INFO)

fh = logging.FileHandler('/tmp/test.log')

ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:%(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

mlogger.addHandler(fh)
mlogger.addHandler(ch)

logger.info('this is info msg')
logger.error('this is error msg')

mlogger.debug('this is debug msg')
mlogger.info('this is info msg')

m2logger = logging.getLogger('com.uk.silence.child')

m2logger.debug('this is debug msg')
m2logger.info('this is info msg')
```

logger说明：
logging.getLogger为默认根logger，logger为树形结构, 在使用m2logger时并为设置hander、formatter、level，但其输出与mlogger相同，原因logger具有继承功能(按名称进行属性继承)

`logger.Filter('com.uk.silence')`用于定义filter功能，表示只有以`com.uk.silence.child`开头的logger进行信息输出,按示例若指定`mlogger.addFilter(filter)`后使用mlogger.error则不能输出日志

handler说明：

|类型|说明|
|---|---|
|logging.StreamHandler|指定向流对象进行|
|logging.FileHandler|指定文件|
|logging.handlers.RotaingFileHandler|指定文件，但可管理文件大小，当超过指定值后则重新创建日志文件
|logging.handlers.TimedRotatingFileHandler|指定文件，超过指定周期后重新创建日志文件|
|logging.handlers.SocketHandler|指定socket|
|logging.handlers.SyslogHandler|指定syslog服务器|
|logging.handlers.HTTPHandler|使用post/get请求提交数据到web服务器|


## logging.config.fileConfig ##

使用文件方式进行日志管理配置，配置文件格式如：

```
[loggers]
keys=root,comuksilence,comuksilencechild

[handlers]
keys=file

[formatters]
keys=basic

[logger_root]
level=WARNING
handlers=file

[logger_comuksilence]
level=INFO
handlers=file
qualname=com.uk.silence
propagate=0

[logger_comuksilencecomchild]
qualname=com.uk.silence.child

[handler_file]
class=FileHandler
formatter=basic
args=('/tmp/test.log')

[formatter_basic]
format=%(asctime)s - %(name)s - %(levelname)s:%(message)s
datefmt=
```
