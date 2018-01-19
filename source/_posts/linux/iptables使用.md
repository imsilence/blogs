title: iptables使用
date: 2015-09-18 12:20:21
tags: [iptables]
categories: [linux]
---

## Netfilter介绍 ##
Netfilter是linux内核提供对报文修改和过滤的框架, 可用于将某些钩子函数作用于网络协议栈, 他本身不对数据包进行过滤, 只是允许过滤数据包和修改数据包的函数挂接到内核网络协议栈的位置, 这些函数是自定义的
Netfilter提供的挂接位置有:
+ 内核空间, 从一个网络接口进来到另一个网络接口去
+ 数据从内核到用户空间
+ 数据从用户空间流出
+ 进入/离开本机的外网接口
+ 进入/离开本机的内网接口

前3个和后2个貌似有些冲突, 已经在网络接口处做了限制为啥还要在内核和用户空间做限制? 因为在网络接口数据包尚未进行路由决策, 不知道下一步去哪里, 因此无法实现数据过滤. 那为啥还要网络接口限制呢? 因为在做NAT和DNAT的时候, 目标地址转换必须在路由之前转换, 示意图:
```
用户空间                                         --------------------->本地进程------------------------
                                                 |                                                    |
*********************************************************************************************************************************************************
内核空间                                         |                                                    |
                                                 |                                               filter output
                                           filter input                                               |
                                                 |                                                [路由决策]
  流入数据包                                     |                                                   \|/                               流出数据包
-------------->nat prerouting-------------->[路由决策]-------------->filter forward------------------->-------------->nat postrouting-------------->
```

Netfilter分别在这五个位置定义了不同的钩子函数叫做五个规则链，只要是数据包经过本计算机必然经过这五个位置之一:
+ PREOUTING: 路由前
+ INPUT: 数据流入口
+ FORWARD: 转发
+ OUTPUT: 数据流出口
+ POSTROUTING: 路由后

## iptables介绍 ##
iptables是liunx提供给用户层的命令接口, 可以通过iptables为Netfilter添加策略, 从而实现报文修改和过滤功能

## 防火墙功能 ##
根据防火墙功能的不同, 引入"表"的概念, 常用的有:
+ filter: 定义允许/允许的功能, 只能在INPUT, FORWARD, OUTPUT三条链中修改 
+ nat: 定义地址转换, 只能在PREROUTING, OUTPUT, POSTROUTING三条链中修改
+ managle: 用于修改数据包，在5条链中都可以实现

目前防火墙主要使用定义策略来定义功能，主要分阻止和接收两种动作, 防火墙根据网络数据包中的信息与依次从前到后与定义的策略中比较, 匹配到一条策略则执行策略定义的动作, 若未匹配则执行默认动作

## 服务控制 ##
目前iptables主要以服务的形式运行在*nix当中, 通过命令: `/etc/init.d/iptables restart/start/stop/status/save` 或 `service iptables restart/start/stop/status/save` 可以控制和产看服务
注意: iptables修改后只对当前系统状态有效, 当系统重启后则失效, 若需要持久有效, 一定要在编辑完成iptables以后使用save命令进行保存

## 练习准备 ##
在对iptables不熟悉的情况下, 防止在配置iptables后, 不能通过ssh服务进行远程登陆的, 可以使用crontab设置定时任务, 每5分钟停止一次iptables服务, 配置命令如下:
`*/5 * * * * /etc/init.d/iptables stop`

## iptables使用 ##
命令格式:`iptables [-t table] COMMAND chain [options] [-j] ACTION`
说明:
+ -t table: 用于指定最那个表操作, 主要是filter, nat, managle, 默认为filter
+ COMMAND: 常用-P(设置默认动作), -A(添加), -D(删除), -I(插入), -R(替换), -L(列举策略), -S(打印策略), -F(删除所策略)
+ chain: 定义策略应用于五个规则链中的哪条上
+ options: 定义数据包中的特征, 比如源ip，目的ip，源端口，目的端口，协议类型等
+ -j: 定义匹配到策略数据包的执行动作, 常用ACCEPT, DROP, REJECT

对于使用iptables修改策略后, 策略会立即生效

例如:
+ 列举所有策略并显示规则号: `iptables -nvL --line-number`
+ 设置INPUT链路默认动作为阻断: `iptables -P INPUT DROP`
+ 添加只有192.168.1.1/24可以使用tcp协议访问本地8080端口: `iptables -A INPUT -s 192.168.1.1/24 -d 0.0.0.0/0 -p tcp --dport=8080 -j ACCEPT`

## COMMAND详解 ##
+ 链路管理
1. -P: 用于设置链路默认处理的动作, 格式: `iptables -P chain ACCEPT/DROP`
2. -F: 清空指定规则链中或所有规则链中的策略，格式: `iptables -F [chain]`
3. -N: iptables允许自定义规则链, 但是自定义的规则链必须与特定的规则链关联，表示当执行特定规则链前首先执行自定义的规则链，当执行完成后再返回到特定规则链中执行, 格式: `iptables -N chain`
4. -X: 删除用户自定义的规则链, 需要注意: 在删除规则链之前需要清空链路中的策略, 格式: `iptables -X chain` 
5. -E: 重命名自定义的规则链, 格式: `iptables -E oname nname`
6. -Z: 将指定链路或者策略中的计数归零, iptables会对每个策略统计匹配到数据包总个数和总大小, 格式: `iptables -Z [chain [rulenum]]` 

+ 策略管理：
1. -A: 添加策略
2. -D: 删除策略
3. -R: 修改策略
4. -I: 插入策略

+ 策略查看
策略查看使用: -L命令, 附加子命令有：
1. -n: 将策略中的ip信息直接打印, 若不添加则会将ip反向域名解析，显示为域名信息
2. -v: 打印详细信息
3. -x: 显示精确信息不对统计数据进行格式化处理
4. --line-num: 显示策略编号

## options详解 ##
+ -s: 指定源ip地址, 必须为ip地址、CIDR或者为0.0.0.0/0.0.0.0表示全部, 可在ip地址之前添加!表示取反操作
+ -d: 表示目的ip地址
+ -p: 表示协议类型, 可使用协议编号或者协议名, tcp, udp, icmp
  扩展参数: 在指定协议类型时, 可以在策略中设置源端口、目的端口、TCP标识位等信息对数据包进行过滤
  1. `-p tcp`扩展:
    a. --dport: 设置目的端口号, 格式: `--dport 80`或者`--dport 1-1024`
    b. --sport: 设置源端口号
    c. --tcp-flag:
  2. `-p udp`扩展:
    a. --dport:
    b. --sport:
  3. `-p icmp`扩展:
    a. --icmp-type: 可设置为0或8，0表示匹配响应的数据包, 8表示匹配请求回显的数据 
    例如, 需要禁用别人ping自己，但是自己可以ping别人时可添加两条策略:
    ```
    iptables -A INPUT -p icmp --icmp-type 0 -j ACCEPT
    iptables -A OUTPUT -p icmp --icmp-type 8 -j ACCEPT
    ```
    对于自己ping自己需要添加:
    ```
    iptables -A INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT
    iptables -A OUTPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT
    ```
+ -i: 指定应用于从某网流入的流量, 格式: `-i eth0`, 一般在chain为PREROUTING和INPUT时使用
+ -o: 指定应用于从某网卡流出的流量, 格式: `-o eth0`, 一般在chain为OUTPUT和PREROUTING时使用
+ -m: 显示扩展
  1.若需要设置端口号为支持多个用逗号分隔的端口可以使用`-m multiport --dport 21,22`
  2.若需要对tcp连接状态进行检测, 比如在tcp连接的三次握手过程中, 连接的状态依次为: LISTENING->NEW->ESTABLISHED, 当发起syn=1 ack=1 rst=1时, 连接不能识别会将状态修改为: INVALID, 在FTP协议中使用20端口作为入口, 21端口作为出口, 但是之间具有关系, 此关系成为RELATED, 我们需要定义值允许NEW和ESTABLISHED状态的数据进入, 只允许ESTABLISHED状态出，则我们添加如此两条策略:
  ```
  iptables -A INPUT -s 0.0.0.0/0.0.0.0 -d 0.0.0.0/0.0.0.0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
  iptables -A OUTPUT -m state --state ESTABLISHED -j ACCEPT
  ```

## -j参数详解 ##
常用的ACTION主要有:
DROP: 表示丢弃, 常用于隐藏服务
REJECT: 明确拒绝
ACCEPT: 接受
custom_chain: 转向自定义规则链
DNAT
SNAT
MASQUERADE: 源地址伪装
REDIRECT: 重定向, 主要用于端口重定向
MARK: 打防火墙标记
RETURN: 返回，在自定义规则链执行完成后返回到源规则链

## DNAT和SNAT ##
+ SNAT: 源地址转换
当内网用户使用同一外网网口进行上网时, 此时需要在外网网口处将数据包的源IP进行修改为外网网口的IP地址, 就可以实现链接外网其他IP地址, 命令:
`iptables -t nat -A POSTROUTING -s sip -j SNAT --to-source source_ip`
当外网IP地址是随机时, 可以使用源地址伪装, 可实现自动寻找外网IP地址并进行修改, 但不一定适合于任何场合
`iptables -t nat -A POSTROUTING -s sip -j MASQUERADE`

+ DNAT: 目的地址转换
目的地址转换的数据流向是从外向内, 常使用外网的IP提供对内网服务的访问, 命令:
`iptables -t nat -A PREROUTING -d dip -p proto --dport dport -j DNAT --to-destination dest_ip`