title: elasticsearch 第三篇(安装篇)
date: 2015-09-15 18:08:21
tags: [elasticsearch]
categories: [存储]
---

## *nux下安装 ##
在*nux下，es官方已提供编译的deb和rpm包，但是需要保证已安装安装java虚拟环境（目前es1.6和1.7版本均可选择1.8版本java），安装步骤如下：
1.[下载ES deb/rpm包](https://www.elastic.co/downloads/elasticsearch "elasticsearch")，并执行安命令
deb包安装: `dpkg -i elasticsearch-1.6.0.deb`
rpm包安装: `rpm -i elasticsearch-1.6.0.rpm`

2.安装后需要将es服务更新随系统启动
+ 对于Debian/Ubuntu系统
执行: `update-rc.d elasticsearch defaults`
系统服务控制: `/etc/init.d/elasticsearch start/stop/restart`

+ 对于redhat/centos系统
执行: `chkconfig -add elasticsearch`
系统服务控制: `service elasticsearch start/stop/restart`

3.若需要修改es启动参数，可直接在/etc/init.d/elasticsearch脚本中修改然后从其服务器

## windows下安装 ##
在windows下es安装比较简单，当然也需要提前安装好java虚拟环境，以下为es安装步骤：
1.[下载zip包](https://www.elastic.co/downloads/elasticsearch "elasticsearch")并解压到安装目录
2.通过es_home/bin/service.bat将es注册到windows服务中(注意需要使用管理员权限运行),service.bat命令格式:`service.bat install|remove|start|stop|manager [server_name]`

|参数|说明|
|----|----|
|install|将es安装到windows服务中|
|remove|将es从windows服务中移除|
|start|服务启动|
|stop|服务停止|
|manager|管理gui|

在未设置安装服务时若未设置server_name时，则命令使用默认名称，在执行service.bat脚本时也不需要指定server_name参数，否则需要手动指定server_name才能执行

3.若需要修改es启动参数，可使用`service.bat manager [server_name]`打开GUI窗口，在"java"选项卡中设置启动参数后重启服务

## es目录解释 ##
```
elasticsearch                     -- path.home, es的安装目录
├─bin                             -- ${path.home}/bin, 启动脚本方式目录
├─config                          -- ${path.home}/config, 配置文件目录
├─data                            -- ${path.home}/data, 数据存放目录
│  └─elasticsearch                -- ${path.home}/data/${cluster.name}
├─lib                             -- ${path.home}/lib, 运行程序目录
├─logs                            -- ${path.home}/logs, log目录 
└─plugins                         -- ${path.home}/plugins, 插件目录
    ├─head
    │  └─...
    └─marvel
        └─...

```

es支持将data目录配置为多个，可通过在进程启动时通过-Des.index.store.distributor设置在存储数据时选择的目录:

|参数值|说明|
|------|----|
|least_used|默认值,选择剩余存储空间最大的目录|
|random|随机选取，选择的概率和目录剩余存储空间大小有关|

该方案提供类似raid0(把连续的数据分散到不同的磁盘存储)的方式,配置也比较简单:
```
path.data: /path/to/data1,/path/to/data2
```

在*nix下使用deb/rpm安装包安装,通常会修改各文件夹的安装路径,默认安装路径如下:

|type|debian/ubuntu|redhat/centos|
|----|-------------|-------------|
|home|/usr/share/elasticsearch|/usr/share/elasticsearch|
|bin|/usr/share/elasticsearch/bin|/usr/share/elasticsearch/bin|
|config(file)|/etc/elasticsearch|/etc/elasticsearch|
|config(env)|/etc/default/elasticseach|/etc/sysconfig/elasticseach|
|data|/var/lib/elasticsearch/data|/var/lib/elasticsearch|
|logs|/var/log/elasticsearch|/var/log/elasticsearch|
|plugins|/usr/share/elasticsearch/plugins|/usr/share/elasticsearch/plugins|