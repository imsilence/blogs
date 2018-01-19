title: zookeeper
date: 2015-08-14 12:51:38
tags: [zookeeper, 分布式共享锁]
categories: [分布式]
---

## 简介 ##

zookeeper为分布式系统调度框架, 用于解决分布式应用中数据管理问题，比如同步锁，分布式应用配置管理等

## 安装&配置 ##

+ [下载](http://mirror.bit.edu.cn/apache/zookeeper/stable/zookeeper-3.4.6.tar.gz)
+ 修改配置
	在conf目录将zoo_sample.cfg拷贝为zoo.cfg, 该文件为zookeeper启动的默认配置文件
	zoo.cfg文件内容:
	```
		tickTime=2000					#zookeeper服务器或客户端与服务器之间发送心跳的时间间隔(2s)
		initLimit=10					#zookeeper集群中连接到leader的fllower的时间不能超过多少个tickTime时间长度，若超过则连接失败
		syncLimit=5					#zookeeper集群中leader和fllower之间发送消息，请求和响应的时间不能超过多少个tickTime时间长度
		dataDir=/tmp/zookeeper				#zookeeper数据存放位置
		clientPort=2181					#zookeeper客户端连接的端口号
		#maxClientCnxns=60				#最大连接数量
		#autopurge.snapRetainCount=3
		#autopurge.purgeInterval=1
		server.A=ipA:portA1:portA2		#表示集群中服务器地址, A:服务器标识, ipA:服务器ip地址, portA1:该服务器与leader通信的端口号, portA2: 当leader挂掉，用来选举使用的端口号
		server.B=ipB:portB1:portB2
	```
	
	在单机部署时至需要配置tickTime,dataDir,clientPort配置即可
	
	在集群部署时需要再设置initLimit,syncLimit,server.*等配置, 同时需要在dataDir目录下新建myid文件, 内容为服务器的标识
	
+ 启动服务器
	`cd ./bin && start zkServer.cmd`
	
+ 启动客户端
	`cd ./bin && start zkCli.cmd -server localhost:2181`
	
+ 集群部署
	1.将zookeeper文件夹拷贝多份,修改zoo.cfg中的clientPort和dataDir
	2.修改dataDir目录下myid文件内容为该服务器的标识
	3.依次启动zookeeper服务器
	
## 实例  ##
使用python实现分布式共享锁

```
#!/usr/bin/env python
#encoding: utf-8

import logging
import threading

import time

from kazoo.client import KazooClient

_logger = logging.getLogger('zlock')

class ZKClient(KazooClient):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ZKClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        super(ZKClient, self).__init__(*args, **kwargs)
        self.start()


class Zlock(object):
    
    def __init__(self):
        self._zkclient = ZKClient(hosts='localhost:2281')
        self._lock_nameservice = '/uk/lock'
        self._lock_prefix = 'lock_id_'
        self._lock_id = ''
        self._event = threading.Event()
    
    def acquire(self, wait=True):
        if self._lock_id == '':
            self._lock_id = self._zkclient.create('%s/%s' % (self._lock_nameservice, self._lock_prefix), str(time.time()), ephemeral=True, sequence=True, makepath=True)
        
        if not self.locked():
            return True
        elif wait:
            self._event.wait()
        else:
            return False
        
    def _watch(self, *args, **kwargs):
        if not self.locked():
            self._event.set()

    
    def release(self):
        self._zkclient.exists(self._lock_id) and self._zkclient.delete(self._lock_id)
        self._lock_id = ''
        self._event.clear()
    
    def locked(self):
        if self._zkclient.exists(self._lock_nameservice):
            _children = self._zkclient.get_children(self._lock_nameservice, self._watch)
            if self._lock_id != '':
                _children.sort()
                return '%s/%s' % (self._lock_nameservice, _children[0]) != self._lock_id
            else:
                return len(_children) != 0
        else:
            return False
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    _lock = Zlock()
    for i in xrange(10):
        print _lock.acquire(True)
        _lock.release()
    pass
```
