title: Docker简介
date: 2015-05-25 23:18:21
tags: [docker]
categories: [虚拟化]
---

## Docker是什么 ##

Docker是基于LXC（Linux容器）实现的一种操作系统级别的虚拟化技术 

## Ubuntu安装 ##

`sudo apt-get install -y docker.io`

## 版本查看 ##

`sudo docker version`        

## 镜象 ##

镜象可以理解为Docker中的一个只读的模板，用来创建容器

+  查找镜象

`sudo docker search registry.hub.docker.com/ubuntu`

+  获取镜象

‵sudo docker pull registry.hub.docker.com/ubuntu:14.04`

+ 列出本地所有镜象

`sudo docker images`

+ 运行镜象创建容器

`sudo docker run -t -i ubuntu:14.10 /bin/bash`

+ 创建镜象

在启动的容器中安装需要的程序后,退出容器(命令exit),使用docker commit将容器创建为镜象

`sudo docker commit -m "add nginx program" -a "Silence UK" container_id ubuntu/nginx:v1`

+ 从本地导入文件创建镜象

模板下载地址: [templates](http://openvz.org/Download/template/precreated)

目前hub.docker.com上提供的镜象为x64,若本地为x86系统,只能从templates下载模板自行创建镜象

`sudo cat ubuntu "ubuntu-14.10-x86.tar.gz" | docker import - ubuntu:14.10`

+ 存入和载出镜象

`sudo docker save -0 ubuntu-14.10.tar ubuntu:14.10`

`sudo docker load --input ubuntu-14.10.tar `

+ 删除镜象

`sudo docker rmi ubuntu:14.10`

+ 原理

利用unionfs（支持将不同目录挂在到同一虚拟文件系统下的文件系统）



## 容器 ##

容器是从镜象创建的运行实例，是一个独立运行的linux环境

+ 启动容器

启动容器有两种方法，一种为根据镜象创建并启动容器，另一种为将已停止的容器重新启动

`sudo docker run -i -t ubuntu:14.10 /bin/bash`

`sudo docker start container_id|container_name`

+ 运行守护

`sudo docker run -d ubuntu:14.10 /bin/sh "while true; do echo hello, docker; sleep 1;done"`

+ 查看log

`sudo docker logs container_id|container_name`

+ 进入容器

`sudo docker attach container_id|container_name`

+ 停止容器

`sudo docker stop container_id|container_name`

+ 查看所有容器

`sudo docker ps -a`

+ 保存和导入容器

`sudo docker export cantainer_id|container_name > nginx.tar`

`sudo cat nginx.tar | docker import - nginx:v1`

+ 删除容器

`sudo docker rm container_id|container_name`


## 仓库 ##

仓库用来做镜象的存储


## 数据管理 ##

+ 数据卷

数据卷是可供一个或多个容器同时使用的特殊目录

`sudo docker run -t -i --name testv -v /home/silence/Documents/github/docker:/tmp/ ubuntu:14.10 python /tmp/t.py`

加载本地磁盘目录/home/silence/Documents/github/docker到容器的/tmp/目录

## 网络 ##

+ 外部访问容器

使用参数-P或-p用于将本地的端口映射到容器的端口上

`sudo docker run -d -p 42001:80 ubuntu:14.10 /bin/bash`


