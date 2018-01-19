title: 记一次修改elasticsearch文件描述符数量
date: 2015-09-16 13:20:21
tags: [elasticsearch]
categories: [存储]
---

背景：在某年某月某日发现es运行不正常，查看日志发现如下错误
```
java.io.IOException: Too many open files
```

以下为操作步骤:
1.查看es节点信息结果:
```
{
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "eE4eHSOWTK-j6IO7JJzcXG" : {
      "name" : "Hardcore",
      "transport_address" : "inet[silence/192.168.1.111:9300]",
      "host" : "silence",
      "ip" : "192.168.1.111",
      "version" : "1.6.0",
      "build" : "cdd3ac4",
      "http_address" : "inet[/192.168.1.111:9200]",
      "process" : {
        "refresh_interval_in_millis" : 1000,
        "id" : 10598,
        "max_file_descriptors" : 32768,
        "mlockall" : false
      }
    }
  }
}

```

疑问：明明在/etc/init.d/elasticsearch启动脚本中设置了`MAX_OPEN_FILES=65535`, 且执行`ulimits -n $MAX_OPEN_FILES`成功, 但是es节点信息中max_file_descriptors始终为32768

2.查看/etc/init.d/elasticsearch启动脚本内容，在启动进程时使用/etc/init.d/functions下的daemon函数启动，最终追溯到daemon使用`runuser -s /bin/bash $user -c "$corelimit >/dev/null 2>&1 ; $*"`方式启动进程，自然想要在-c中添加ulimit -n 65535, 结果以失败告终，启动脚本报错`ulimit: open files: cannot modify limit: Operation not permitted`，自己在命令行下发现普通用户在修改时报错, 而root用户就ok

3.修改/etc/security/limits.conf文件添加如下内容(es运行用户为elasticsearch)
```
elasticsearch        hard     nofile         65535
elasticsearch        soft     nofile         65535
```

修改内容后重启es, 启动后查询es节点信息max_file_descriptors还是为32768 ... 此时已疯

4.查看谷歌，说/etc/pam.d/login文件中需要有`session     required      pam_limits.so` limits.conf文件才会起效，于是乎，我加上了，结果...尼玛咋还是32768呢
5.再次查看/etc/pam.d/login发现有这么一句话`session    include      system-auth`, 一看就是导入了文件system-auth, 于是在system-auth中发现已经存在`session     required      pam_limits.so`，然后尼玛删除步骤3添加的内容
6.此时想到反编译pam_limits.so文件看看到底干了什么事, 当然先得查询文件在哪 `find / -name pam_limits.so`
然后使用`strings pam_limits.so` 结果尼玛发现其中有这么两行:
```
/etc/security/limits.conf
.
.
.
/etc/security/limits.d/*.conf
```
自然想查看/etc/security/limits.d/下的*.conf结果，发现了def.conf，内容为:
```
*        hard     nofile         32768
*        soft     nofile         32768
```
说明: *表示对所有用户生效

结果自然要试试修改def.conf文件，结果这次ok了

分析原因：
1.why在/etc/init.d/elasticsearch中已经设置ulimit -n为啥没有生效
runuser命令格式:`runuser -s [shell] [uid/gid] -c "command"`, 说明:使用一个替代的用户或组ID运行一个Shell, 只有会话的PAM hooks运行, 并且没有密码提示, 这个命令仅在root用户时有用
根据测试也知道ulimit -n只是修改当前会话中的打开文件描述符数量, 当打开新回话时或切换新用户则失效。并根据描述得知runuser在打开会话之后PAM hooks认证模块会执行，因此在此前的设置参数都无效

2.why在runuser时在-c中添加ulimit -n 65535报错
查找资料发现, 普通用户在设置ulimit -n时其大小不能超过预设置的值, 那预设置的值是谁呢, 自然就想到limits.conf，可以自己测试在limits.conf中添加自己的用户信息(silence is me)，可以发现再次修改则正常
```
silence        hard     nofile         65535
silence        soft     nofile         65535
```

3.limits.conf和limits.d/*.conf的关系
此时自然想到的是文件加载顺序和配置内容有关，配置相同的内容但是值不通时，后加载的配置文件的值会生效呢, 我们做一下测试:在limits.d/def.conf配置文件中添加一下信息，因为第2步已经在limit.conf中设置其值为65535并测试成功，那么此时若我们再测试`ulimit -n 50000`正常而`ulimit -n 65535` 不正常自然可以验证我们的猜测
```
silence        hard     nofile         50000
```
结果自然与猜测一致
根据反编译的结果pam_limits.so会先加载limits.conf然后再加载limits.d/*.conf此时有一定顺序, 但是limits.d/*.conf中加载顺序如何呢? 猜测与系统排序有关，但未测试，在通常情况下好的系统管理员对不同用户应该根据userid在limits.d下建立不同的文件单独配置，方便管理
为什么在limits.d/def.conf中值设置hard值呢？可以查看配置文件的规则，hard设置为允许修改的最大值而soft设置的是新回话生成时默认设置

4.此时你应该会问这个值到底可以设置多大?
查看文件/proc/sys/fs/file-max和/proc/sys/fs/file-nr内容
输入: `cat /proc/sys/fs/file-max`
输出: `191832`

输入: `cat/proc/sys/fs/file-nr`
输出: `1792  0 191832`

查阅GOOGLE, file-nr文件中的三个数分别表示: 系统已经分配的文件句柄数, 没有用到的句柄数和所有可分配的最大句柄数，file-max中的值为最大所能分配的句柄数, 因此在ulimit -n是设置的值不能超过file-max记录的值
file-nr文件内容通常由在系统启动时根据系统内存计算得出，系统内存增大则file-max增大

5.如何查看其他进程当前设置的max_file_descriptors
对于linux内核为2.6.24及以后版本
输入: `cat /proc/34690/limits | grep "Max open files"`
输出: `Max open files            32768                32768                files`

6.如何查看某进程当前打开的文件句柄数:
输入: `lsof -n|awk '{print $2}'|sort|uniq -c|sort -nr|grep pid`
输出: `cnt pid`