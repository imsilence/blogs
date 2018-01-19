title: elasticsearch 第二篇(配置篇)
date: 2015-09-15 13:55:21
tags: [elasticsearch]
categories: [存储]
---

## 配置 ##
在es启动之前可以通过设置启动命令行启动参数、环境变量、文件等方式优化和配置es进行参数

## 环境变量 ##

|名称|示例|说明|
|----|----|----|
|ES_MIN_MEM|256M|用于配置java进程分配的最小内存|
|ES_MAX_MEM|1G|用于配置java进程占用的最大内存|
|ES_HEAP_SIZE|32G|设置ES_MIN_MEM,ES_MAX_MEM使用相同大小,ES推荐该配置并启用mlockall|
|ES_DIRECT_SIZE|2G|直接内存并不是虚拟机运行时数据区的一部分,在nio中引入了基于通道和缓冲区的I/O方式,它可以使用native函数直接分配堆外内存,然后通过存储在java堆中的DirectByteBuffer对象作为这块内存的引用进行操作|
|ES_USE_IPV4|not empty/empty|表示只使用IPV4, 若定义且值不为空则表示true|

## 系统配置 ##
+ 设置系统允许打开的文件描述符数量，建议设置为32k或64k, 可通过命令ulimit -n进行查询，示例:`ulimit -n 65535`后重启服务
可以在启动时添加参数-Des.max-open-files=true查看允许打开的文件描述符数量

也可以通过RESTAPI查看nodes信息，输入:`GET /_nodes/process?pretty`
输出:
```
{
   "cluster_name": "elasticsearch",
   "nodes": {
      "eE4eHSOWTK-j6IO7JJzcDQ": {
         "name": "Specialist",
         "transport_address": "inet[silence/192.168.1.111:9300]",
         "host": "silence",
         "ip": "192.168.1.111",
         "version": "1.6.0",
         "build": "cdd3ac4",
         "http_address": "inet[/192.168.1.111:9200]",
         "process": {
            "refresh_interval_in_millis": 1000,
            "id": 6212,
            "max_file_descriptors": -1,
            "mlockall": false
         }
      }
   }
}
```

## 虚拟内存设置 ##
es采用混合的mmapfs/niofs目录默认存储索引，在mmap计数太低时可能导致存储器异常，可通过sysctl vm.max_map_count查询，需要设置使用命令`sysctl -w vm.max_map_count=262144`或者在/etc/sysctl.conf中进行永久设置

## 内存设置 ##
在操作系统为尽量多的使用内存，会将不用的应用程序内存换出存储在swap文件系统中，交换会降低系统的性能和节点的稳定性，需要禁止，可通过三种方法进行设置：
+ 禁用swap分区
在linux中可通过`swapoff -a`或在/etc/fstab中注释所有行中swap的内容
在windows中在"系统属性"->"高级"->"性能"->"高级"->"虚拟内存"中设置

+ 配置swappiness
通过sysctl vim.swappiness=0减少内核进行的swap交换

+ mlockall
在*nux上使用mlockall或者在window上使用VirtualLocx尽量锁定进程的地址空间到RAM，防止es内存被换出，可通过elasticsearch.yml进行配置
在es配置文件中添加:`bootstrap.mlockall: true`并重启服务即可

通过RESTAPI查看nodes信息，输入:`GET /_nodes/process?pretty`

在*nux系统下可能有两个原因导致mlockall设置失败：
1.es进程所属用户不具有锁定内存的权限，需要使用ulimit -l进行设置
2./tmp目录设置了noexec选项，可通过在启动es时设置-Djna.tmpdir=/path/to/new/dir解决

# es配置 ##
在ES_HOME/conf目录下两个配置文件分别为elasticsearch.yml和logging.yml, elasticsearch.yml为es所有模块提供配置, logging.yml为日志记录提供配置

+ elasticsearch.yum解读

1.network设置
network.host: 设置bind host和publish 
2.path设置
path.logs: 设置日志存储目录
path.data: 设置数据存储目录
3.cluster设置
cluster.name: 设置集群标识
4.node设置
node.name: 设置节点标识
5.index设置
es支持创建存储到内存中的索引，可以在创建索引或者在进程启动时指定默认存储方式
a.在yum配置文件中配置index.store.type:memory
b.在es进程启动时通过参数-Des.index.store.type=memory设置
c.在创建index时通过参数提交，输入:
```
PUT http://localhost:9200/m_index_test2/
{
  "index" :{
      "store": {
        "type": "memory"
      }
  }
}
```
说明：存储在内存中的索引在重启服务器后数据会丢失

6.在yum配置文件中可设置为环境变量的引用，比如在环境变量中定义节点的名称ES_NODE_NAME, 则可在yum配置文件中设置node.name=${ES_NODE_NAME}
7.可在es进程启动时通过进程启动参数进行设置,如-Des.node.name=silence
8.可以在es进程启动时通过-Des.config=/path/to/config/file重新指定config文件

+ logging.yum配置可参考[log4j](http://logging.apache.org/log4j/1.2/manual.html 'log4j')