title: centos7.0 iptables使用
date: 2015-10-15 18:20:21
tags: [centos, iptables]
categories: [linux]
---

在centos7.0默认使用firewalld服务，若萱使用iptables，需要禁用firewalld并启动iptables

systemctl stop firewalld
systemctl disabled firewalld

安装 iptables

yum install iptables-services
systemctl enbale iptables

cp /usr/libexec/iptables/iptables.init /etc/init.d/iptables

service iptables save
service iptables stop
service iptables start

systemctl stop iptables
systemctl start iptables
