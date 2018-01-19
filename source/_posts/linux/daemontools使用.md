title: daemontools使用
date: 2015-10-08 17:08:21
tags: [进程监控]
categories: [linux]
---

1. [下载](http://cr.yp.to/daemontools.html daemontools)
2. 安装
```
tar xvzf daemontools-0.76.tar.gz
cd admin/daemontools-0.76
package/install
```
若报错`/usr/bin/ld: errno: TLS definition in /lib64/libc.so.6 section .tbss mismatches non-TLS reference in envdir.o`, 则修改代码admin/daemontools-0.76/src/error.h中的extern int errno;替换为#include <errno.h>

3. 启动

使用命令`svscanboot &`来启动svscan工具

查看进程`ps -aux | grep svscan`

自启动配置参考: [http://cr.yp.to/daemontools/start.html](http://cr.yp.to/daemontools/start.html start)

在完成后会自动在/etc/inittab中添加`SV:123456:respawn:/command/svscanboot`，若重启机器后svscan未启动则需要删除该行并在/etc/init目录下创建svscan.conf并添加内容
```
start on runlevel [123456]
stop on runlevel [^123456]
respawn
exec /command/svscanboot
```
对于centos系统可参考:[http://www.productionmonkeys.net/guides/qmail-server/daemontools] (http://www.productionmonkeys.net/guides/qmail-server/daemontools)

4. 配置

创建服务目录并配置启动文件
```
mkdir /opt/svc/servername
cat /opt/svc/servername/run

#!/bin/sh
exec /home/server_image_bin

ln /opt/svc/servername/ /service/
```

5. 命令使用
svc -u /service/servername
svc -d /service/servername
svc -dx /service/servername && rm /service/servername

svstat services 

注意:
使用daemontools管理的进程不能以daemon方式运行