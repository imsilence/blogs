title: elasticsearch 第五篇(文档操作接口)
date: 2015-09-17 13:46:21
tags: [elasticsearch]
categories: [存储]
---

## INDEX API ##
示例:
```
PUT /test/user/1
{
  "name": "silence",
  "age": 27
}
```
说明:
1.索引文档使用PUT方法，需要指定index(test)、type(user)和文档编号，提交数据为json格式为文档的内容
2.在索引文档时，会自动检查index和type是否存在，若不存在则自动创建，对于type会自动调用putmapping方法为type自动创建mapping，当提交的json数据新增字段时也会自动对type自动调用putmapping方法在mapping中添加新的字段类型
可通过elasticsearch.yml中添加配置禁用自动创建index和type
```
action.auto_create_index: false        #禁用自动创建index
index.mapper.dynamic: false            #禁用自动生成type
```
在某些时候允许某类型或者禁用某类型的index自动创建，则可以使用匹配模式和黑白名单形式进行配置

```
action.auto_create_index: +test*,+temp*,+tmp*       #只允许自动创建以test,temp,tmp开头的index
```
说明: 若action.auto_create_index设置为true或允许某些index执行, index.mapper.dynamic设置为false, 则可第一次时index自动创建一个type，后续不能再单独创建新的type

3.文档中的version属性
es为每个文档自动设置一个version属性, version从1开始, 当文档发生更新，删除操作时version都会自增1, version是范围为[1, 9.2e+18]的整数, 在获取或查询文档是version作为文档的一部分返回
version属性主要使用乐观锁机保证数据在读取后再进行更新动作时的数据一致性问题，在提交请求时通过指定version参数表示存储的版本必须符合条件时才可执行成功, 默认条件为两者一致，若不提交version表示不进行检查
使用方法:
例如编号为1的文档version为7
```
{
   "_index": "test",
   "_type": "user",
   "_id": "1",
   "_version": 7,
   "found": true,
   "_source": {
      "name": "silence",
      "age": 27
   }
}
```
当我们使用如下请求执行更新动作可看到执行成功，并且version自增1, 返回结果中为8:
输入:
```
PUT /test/user/1?version=7
{
  "name": "silence",
  "age": 28
}
```
输出:
```
{
   "_index": "test",
   "_type": "user",
   "_id": "1",
   "_version": 8,
   "created": false
}
```

当我们再次发出version=7的请求得到的响应为:
```
{
   "error": "VersionConflictEngineException[[test][2] [user][1]: version conflict, current [8], provided [7]]",
   "status": 409
}
```
可自己测试version>8的请求依然失败, 此时你可能会想到在高并发情况下此种效率是否会低效, 可能你会在内存中放置一个version+1的副本, 通过内存中对副本进行自增, 然后异步方式提高并发, 此时执行成功率会下降并且导致数据丢失, 在此种情况下只要满足你指定的version大于存储中的版本号即可, 为解决此种问题es提供version_type可以指定使用的比较策略：

|version_type值|说明|
|--------------|----|
|internal|默认值, 表示指定version必须与存储中的version一致, 若成功则存储version自增1|
|external/external_gt|指定值必须大于存储中的version, 若成功存储version设置为提交的version|
|external_gte|指定值必须大于等于存储中的version, 若成功存储version设置为提交的version|
|force|强制更新，并将存储version设置为提交的version|

4.op_type: 在提交请求时指定op_type=create, 表示若id不存在时创建, 否则失败
输入
```
PUT /test/user/1?op_type=create
{
  "name": "silence",
  "age": 28
}
```
输出:
```
{
   "error": "DocumentAlreadyExistsException[[test][2] [user][1]: document already exists]",
   "status": 409
}
```
op_type=create的另一种表示方法为:
```
PUT /test/user/1/_create
{
  "name": "silence",
  "age": 28
}
```

5.ID生成器: 在大多数情况下我们不需要维护也不关心文档的id是什么, 在es中可以为文档自动生成id，方式为使用post方式提交参数, 并在请求中不指定id值(若指定则使用指定的id值)
6.routing路由分配: 在创建index时通常会将index数据存放在不同的shard上，es默认通过hash(id) % shard_num决定将文档存储在哪个shard上，此刻你应该想到routing的作用，对，就是用来指定做负载是hash的输入参数:
输入:
```
POST /test/user/?routing=name
{
  "name": "silence",
  "age": 28
}
```

若在索引文档时显示指定routing，则在提交文档中必须存在指定routing对应的值，否则执行失败

7.分布式执行
索引操作会被路由到shard上，并在包含该shard的node中执行，若存在复制shard，则当所有复制节点从主shard中执行成功后，返回结果

8.一致性
为防止某些网络节点错误，默认情况下当索引成功数量>=仲裁(replicas/2+1)时，则认为操作成功，对于复制数量为1时则数据一共存两份（主shard和复制shard），此时若主shard写成功则认为执行成功
可在elasticsearch.yml中将action.write_consistency设置为one,all,quorum修改判断依据

9.刷新shard
为了在索引文档成功后立即查询到文档(当shard刷新后才可search到), 可以通过设置refresh=true在索引文档成功后立即执行存储该数据shard的刷新动作, 在设置前应该对索引和查询进行对性能测试，对于get接口获取文档是完全实时的

再次分享自己趟过的一个坑:
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

各位看着有问题吗？好吧，貌似没有问题，但是呢执行完成后，你会惊奇的发现es中你的统计的数据里面存储大量重复的ip，问题原因大家已经知道了吧

解决方法：我在内存中做了一个缓存，通过缓存去重，当在缓存中不存在时则放入缓存中并存储到es

10. timeout
当文档被索引时会从主shard将数据复制到复制shard, 主shard需要等待复制shard的响应后返回执行结果, 此等待时间默认为1min, 可以通过在请求中添加timeout修改此时间

## GET API ##
示例:
输入:
`GET /test/user/1`
输入:
```
{
   "_index": "test",
   "_type": "user",
   "_id": "1",
   "_version": 3,
   "found": true,
   "_source": {
      "name": "silence",
      "age": 28,
      "book": {
         "name": "迷失的自己"
      }
   }
}
```
说明:
1.可以通过GET方法根据文档的ID读取文档内容
_index,_type,_id三元组唯一标识一个文档, 分别表示索引，类型和文档id
_version为文档的版本
found表示是否查询到结果, true表示存在, false表示不存在
_source是真正的文档内容

2.可以通过HEAD方法根据reponse header信息判断文档是否存在
输入:`curl -XHEAD -i "http://localhost:9200/test/user/1"`
```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8
Content-Length: 0`
```
输入:`curl -XHEAD -i "http://localhost:9200/test/user/1`
输出:
```
HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=UTF-8
Content-Length: 0
```

可以看到若文档存在使用HEAD方法则返回状态码为200，否则状态码为404

3.GET操作默认是实时的，也就是说文档索引后可立即读取，并不像Search需要等待shard刷新，但是通过在GET请求中通过参数realtime=false或者在elasticsearch.yml配置action.get.realtime:false禁用
4.在GET数据时可以使用"_all"替代要查询的_type, 此时会返回在所有type中第一个匹配到的document
5.在GET数据时可以通过_source, _source_include & _source_exclude设置返回文档包含的属性
输入: `GET /test/user/1?_source=false` 不返回任何_source内容
输入: `GET /test/user/1?_source=name` 只返回_source中的name
输入: `GET /test/user/1?_source_include=*.name&_source_exclude=name`

_source常用于需要返回一两个字段的情况, 内容较多的文档属性值进行筛选时可以组合_source_include和_source_exclude
6.若只想返回_source中的内容可以使用:`GET /test/user/1/_source`
7.若在索引文档时指定了routing_key为了可以正确GET到文档,则需要在GET请求中添加routing指定正确的routing_key
8.默认GET文档执行在复制shard的上，但可以通过设置preference为_primary或者_local, _primary表示在主shard上执行, _local表示在一个分配且可用的shard上执行
9.GET请求中也可以添加refresh=true参数强制使获取文档相关shard刷新, 从而可以被search到
10.在GET请求发出后，会根据需要获取文档id将请求转发到一个相关的复制节点上执行并返回结果
11.可以在GET请求中指定version属性用于需要获取符合规则version的文档

## DELETE API ##
示例:
输入
`DELETE /test/user/1`

说明:
1.在DELETE方法提交的参数中可以设置version属性用于删除符合规则的version文档
2.当在index文档是设置routing_key, 那么在删除文档时也需要使用routing设置正确的routing_key
3.当删除文档是若index不存在, 则es会自动创建
4.删除文档请求会被转发到主shard上, 主shard操作完成后, 各复制shard会从主shard进行同步
5.