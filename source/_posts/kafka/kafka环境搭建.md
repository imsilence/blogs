title: kafka环境搭建
date: 2015-10-13 23:18:21
tags: [kafka]
categories: [消息队列]
---

## 启动 ##

  cd /d "D:/ProgramFiles/Kafka/bin/windows/"

  start zookeeper-server-start.bat "D:/ProgramFiles/Kafka/config/zookeeper.properties"

  start kafka-server-start.bat "D:/ProgramFiles/Kafka/config/server.properties"
    
   
## 启动集群 ##

  1.修改server.properties中的broker.id, port, log.dirs属性值，并另存为server_{port}.properties
  
  2.start kafka-server-start.bat "D:/ProgramFiles/Kafka/config/server_{port}.properties"

## 停止 ##

  cd /d "D:/ProgramFiles/Kafka/bin/windows/" && kafka-server-stop.bat
  
  cd /d "D:/ProgramFiles/Kafka/bin/windows/" && zookeeper-server-stop.bat

## topic ##

+ 创建topic

  kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
  
+ 查看topic

  kafka-topics.bat --describe --zookeeper localhost:2181
  
  kafka-topics.bat --list --zookeeper localhost:2181

## 测试 ##

  start kafka-console-producer.bat --broker-list localhost:9092 --topic test
  
  start kafka-console-consumer.bat --zookeeper localhost:2181 --topic test --from-beginning

## 问题 ##

  1. 在kafka客户端连接集群时，kafka会返回给客户端所有集群的MetadataResponse信息(集群中所有的节点)，由客户端选择使用哪个节点通信
  并且可通过配置host.name和advertised.host.name指定

  2. kafka的log数据不能放在tmp目录，小心由于机器重启后导致数据缺失混乱，此时客户端连接时会报NoLeaderAvailableError