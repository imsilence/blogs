title: windows安装mysql zip包
date: 2015-09-18 12:20:21
tags: [mysql]
categories: [存储]
---

1. 修改my.ini文件
mysqld节点下添加
basedir = D:\MySQL\MySQL5.7
datadir = D:\MySQL\datas
port = 3306

注意datadir不能在basedir下

2. 初始化系统数据库
mysqld --initialize-insecure --explicit_defaults_for_timestamp

3. 安装服务
mysqld install MySQL57 --defaults-file=D:\MySQL\MySQL5.7\my.ini

4. 启动服务
net start MySQL57

5. 设置root密码
默认root密码为空可以使用mysql -u root -p, 输入回车直接进入mysql交互环境
可以使用mysqladmin命令修改root密码, mysqladmin -u root -p password XXX