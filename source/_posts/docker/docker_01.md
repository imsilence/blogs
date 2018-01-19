title: Docker安装
date: 2015-10-28 10:55:21
tags: [docker]
categories: [容器]
---

## CentOS 7.0 Docker安装 ##

系统要求:
x64 cpu架构, linux内核版本>=3.10, 开启cgroups和namespace

命令查询:
1. x64cpu架构查询
输入: `uname -m`
输出: `x86_64`

2. linux内核查询
输入: `uname -r`
输出: `3.10.0-229.el7.x86_64`

安装:
1. 添加docker源
```
cat > /etc/yum.repos.d/docker.repo <<EOF
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
```

2. 安装docker:
```
yum install -y docker-engine docker-selinux
```

可能由于网络原因在下载源或者gpgkey时失败, 可以使用其他工具手动下载然后将docker-engine的包拷贝到yum cache目录, 然后在使用yum install安装
a. 源下载失败:
```
wget https://yum.dockerproject.org/repo/main/centos/7/Packages/docker-engine-1.8.3-1.el7.centos.x86_64.rpm -O docker-engine-1.8.3-1.el7.centos.x86_64.rpm

# cache目录: /var/cache/yum/x86_64/7/dockerrepo/packages/
cp docker-engine-1.8.3-1.el7.centos.x86_64.rpm /var/cache/yum/x86_64/7/dockerrepo/packages/
```
b.gpgkey下载失败
可以将repo配置中的gpgcheck=1改为gpgcheck=0表示不对源进行检查


3. 启动docker daemon
```
sudo service docker start
```
在centos7.0会发现不能重启服务, 测试应该为centos7.0默认使用firewalld防火墙与docker在网络方面产生某些冲突, 未深揪, 但是安装docker-selinux后可以重启, 但是当firewalled在docker daemon之后重启, docker的网络就会有问题, 原因是firewalld在启动时会删除docker在iptables中添加的规则
在测试环境可以选择停用firewalld而是用iptables
```
systemctl stop firewalld
systemctl disable firewalld
```

4. 添加当前用户到docker组总
```
sudo usermod -aG docker $USER
```

5. 添加docker daemon随机启动
```
sudo chkconfig docker on
```

6. 测试
```
docker info
```

7. 卸载

```
#查看安装的docker包
yum list installed | grep docker

#根据查询的安装包进行卸载
sudo yum -y remove docker-engine.***

#删除所有镜像、容器和卷
rm -rf /var/lib/docker

#删除配置信息
```

## Ubuntu 安装 ##

```
wget -qO- https://get.docker.com/gpg | sudo apt-key add -

wget -qO- https://get.docker.com/ | sh

sudo usermod -aG docker ${USER}
```

重新开启shell