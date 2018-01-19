title: 记一次elasticsearch索引数据后但查不到
date: 2015-09-17 18:46:21
tags: [elasticsearch]
categories: [存储]
---

背景:需要在一堆日志中统计所有存在的源IP，日志时按天存放的，代码结构如下：
```
def get_all_store_hosts():
   '''
      返回es中存储中所有ip
      在索引doc时未设置refresh
   '''
   return _all_

def get_distinct_hosts_from_logs(day):
   '''
      从日志中查询所有的ip并去重
   '''
   return _hosts_

def store_hosts(hosts)
   '''
   将新的ip存储到es中
   '''

def stat(day):
   _all_ = get_all_store_hosts()
   _hosts_ = get_distinct_hosts_from_logs:
   _hosts_ = [_host for _host in  _hosts_ if _host not in _all_]
   if len(_hosts_):
      store_hosts(_hosts_)

if __name__ == '__main__':
   for day in xrange(1, 30):
      stat(day)
```

各位看官觉得有问题吗？好吧，貌似没有问题，但是呢执行完成后，你会惊奇的发现es中你的统计的数据里面存储大量重复的ip

问题原因:
在文档索引的shard上到shard更新有一定时间间隔, 而只有到shard更新后才可search到文档, 也就是说文档索引后不一定可以查询到, 在es的官方文档中亦有描述，戳[这里查看Refresh一节](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html#index-refresh 'es关于索引的refresh属性描述'), 文档亦给出解决方法在索引时使用refresh=true属性, 但是需要测试对索引和查询性能的影响

在这里我的解决方法：在内存中做了一个缓存，通过缓存去重，当不缓存中不存在时则存储到es，并放入缓存中，为什么可以放在内存中，原因，就算有40w的ip, 放在内存数组中时, 内存大小占用25M左右对于一般的机器足以承受