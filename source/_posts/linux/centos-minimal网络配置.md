title: centos minimal网络配置
date: 2015-09-22 10:20:21
tags: [centos, network]
categories: [linux]
---

centos 6.7mnimal是centos提供的最小安装盘, 其网卡默认不启动
1.修改配置文件: `/etc/sysconfig/network-script/ifcfg-eth0`为`ONBOOT=yes`和`NM_CONTROLLED=no`
2.重启网卡: service network restart


centos 7.1mnimal是centos提供的最小安装盘, 其网卡默认不启动
1.修改配置文件: `/etc/sysconfig/network-script/ifcfg-nep0s3`为`ONBOOT=yes`
2.重启网卡: `service network restart`
3.安装网络管理工具: `yum install net-tools`