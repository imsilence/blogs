title: elasticsearch 第四篇(API约定)
date: 2015-09-16 15:46:21
tags: [elasticsearch]
categories: [存储]
---

## 对多个indices进行操作 ##
es中大多resetapi支持请求多个index, 例如"test1,test2,test3"，index也可以使用通配符, 例如"test\*", 还可以使用+,-来包含或移除某个或某类index, 例如"test\*,-test1"
支持设置多个的api的请求字符串可设置以下参数:
+ ignore_unavailable: 是否忽略单个index是否可用(不存在或关闭), true表示忽略, false表示不忽略, 默认为false, 例如查询已经关闭的index:

输入: `GET /test1/user,account/_search?ignore_unavailable=false`
输出:
```
{
   "error": "IndexClosedException[[test1] closed]",
   "status": 403
}
```

输入: `GET /test1/user,account/_search?ignore_unavailable=false`
输出:
```
{
   "took": 1,
   "timed_out": false,
   "_shards": {
      "total": 0,
      "successful": 0,
      "failed": 0
   },
   "hits": {
      "total": 0,
      "max_score": 0,
      "hits": []
   }
}
```

+ allow_no_indices: 是否忽略通配符匹配不到index(不存在或关闭)的情况, true表示允许, false表示不允许，默认为true, 例如查询已经关闭的index:

输入: `GET /test*/_search?allow_no_indices=false`
输出: 
```
{
   "error": "IndexMissingException[[test*] missing]",
   "status": 404
}
```

输入: `GET /test*/_search?allow_no_indices=true`

```
{
   "took": 1,
   "timed_out": false,
   "_shards": {
      "total": 0,
      "successful": 0,
      "failed": 0
   },
   "hits": {
      "total": 0,
      "max_score": 0,
      "hits": []
   }
}
```

+ expand_wildcards: 设置是否扩展通配符到closed的index中，open表示只在匹配并为open的index中查询，closed表示在匹配的所有的index中查询, 默认为closed, 例如查询已经关闭的index
输入: `GEt /test*/_search?expand_wildcards=closed`
输出:
```
{
   "error": "IndexClosedException[[test1] closed]",
   "status": 403
}
```

## 公共参数 ##

+ format: 表示返回数据的格式, 可选值为yaml和json两种, 例如:
输入: `GET /test1/user/_search?format=yaml`
输出:
```
---
took: 23
timed_out: false
_shards:
  total: 5
  successful: 5
  failed: 0
hits:
  total: 1
  max_score: 1.0
  hits:
  - _index: "test1"
    _type: "user"
    _id: "1"
    _score: 1.0
    _source:
      name: "silence"
```

+ pretty: 表示在已json格式返回数据时是否以可视化的格式返回, false或未在设置表示不格式化, 否则格式化

+ human: 表示是否对返回结果进行格式化处理，比如3600(s)显示1h

+ 查询结果过滤
主要使用filter_path参数进行设置

1.在返回结果中我们只关注took, hits.total, hits.hits._id, hits._source, 则我们可以发起如此请求:
输入:`GET /test1/user/_search?filter_path=took,hits.total,hits.hits._id,hits.hits._source`
输出:
```
{
   "took": 1,
   "hits": {
      "total": 1,
      "hits": [
         {
            "_id": "1",
            "_source": {
               "name": "silence"
            }
         }
      ]
   }
}
```

2.也可以使用统配符进行设置
输入: `GET /_nodes/stats?filter_path=nodes.*.*ost*,nodes.*.os.*u`
输出:
```
{
   "nodes": {
      "9jfW4VeWRta-Uq7Cq7bK34": {
         "host": "silence",
         "os": {
            "cpu": {
               "sys": 1,
               "user": 1,
               "idle": 96,
               "usage": 2,
               "stolen": 0
            }
         }
      }
   }
}
```

3.若层级较多时可使用\*\*进行简化
输入: `GET /_nodes/stats?filter_path=nodes.**.*sys*`
输出:
```
{
   "nodes": {
      "9jfW4VeWRta-Uq7Cq7bK34": {
         "os": {
            "cpu": {
               "sys": 2
            }
         },
         "process": {
            "cpu": {
               "sys_in_millis": 139106
            }
         }
      }
   }
}
```

4.若只需要_source中的某些值，则可以将filter_path和_source参数共同使用
输入: `GET /test1/account/_search?filter_path=hits.hits._source&_source=firstname,lastname,gender&size=2`
输出:
```
{
   "hits": {
      "hits": [
         {
            "_source": {
               "firstname": "Rodriquez",
               "gender": "F",
               "lastname": "Flores"
            }
         },
         {
            "_source": {
               "firstname": "Opal",
               "gender": "M",
               "lastname": "Meadows"
            }
         }
      ]
   }
}
```

5.flat_settings用于设置在查询setting时,setting中的key格式, 默认为false:
输入: `GET /test1/_settings?flat_settings=true`
输出:
```
{
   "test1": {
      "settings": {
         "index.creation_date": "1442230557598",
         "index.uuid": "70bg061IRdKUdDNvgkUBoQ",
         "index.version.created": "1060099",
         "index.number_of_replicas": "1",
         "index.number_of_shards": "5"
      }
   }
}
```

输入: `GET /test1/_settings?flat_settings=false`
输出:
```
{
   "test1": {
      "settings": {
         "index": {
            "creation_date": "1442230557598",
            "number_of_shards": "5",
            "uuid": "70bg061IRdKUdDNvgkUBoQ",
            "version": {
               "created": "1060099"
            },
            "number_of_replicas": "1"
         }
      }
   }
}
```

+ 请求参数格式
1.boolean: 在es中将"0", 0, false, "false", "off"识别为false，其他均按ture处理
2.number
3.time: 可以提交一个以毫秒时间的整数或者以日期标识结尾的字符串，例如"2d"表示2天，支持的格式有: y(year),M(month),w(week),d(day),h(hour),m(minute),s(second)
4.距离: 可以提交一个以米为单位的证书或者以距离表示结尾的字符串，例如"2km"表示2千米，支持的格式有: mi/miles(mile英里), yd/yards(yard码), ft/feet(feet尺), in/inch(inch英寸), km/kilometers(kilometer千米), m/meters(meter米), cm/centimeters(centimeter厘米), mm/millimeters(millimeter毫米), NM/nmi/nauticalmiles(Nautical mile纳米)
5.模糊类型: 
	a.数字,时间, IP：类似于range -fuzzines<=value<=+fuzzines
	b.字符串: 计算编辑距离

+ 返回结果中key的格式为驼峰还是下划线分割, 通过case设置为camelCase则返回驼峰格式，否则为下划线分割形式
+ jsonp: 可以用jsonp回调的方式调用es api, 需要通过callback设置回调函数名称，并且需要在elasticsearch.yml中配置`http.jsonp.enable: true`来启用jsonp格式

## url访问控制 ##
可以通过代理方式进行es的url访问控制，但是对于multi-search，multi-get和bulk等在请求参数中设置不同的index的情况很难解决.
为防止通过请求体设置index的情况,需要在elasticsearch.yml中设置`rest.action.multi.allow_explicit_index:false`, 此时es不允许在request body中设置index

如在修改前：
输入:
```
POST /test1/user3/_bulk?pretty
{"index" : {"_index" : "test2", "_type" : "user1", "_id" : 1}}
{"name" : "silence1"}
{"index" : {"_index" : "test2", "_type" : "user1", "_id" : 2}}
{"name" : "silence2"}
```
输出:
```
{
   "took": 225,
   "errors": false,
   "items": [
      {
         "index": {
            "_index": "test2",
            "_type": "user1",
            "_id": "1",
            "_version": 1,
            "status": 201
         }
      },
      {
         "index": {
            "_index": "test2",
            "_type": "user1",
            "_id": "2",
            "_version": 1,
            "status": 201
         }
      }
   ]
}
```


如在修改后(已重启)：
输出:
```
{
   "error": "IllegalArgumentException[explicit index in bulk is not allowed]",
   "status": 500
}
```

输入:
```
POST /test1/user3/_bulk?pretty
{"index" : {"_id" : 1}}
{"name" : "silence1"}
{"index" : {"_id" : 2}}
{"name" : "silence2"}
```
输出:
```
{
   "took": 8,
   "errors": false,
   "items": [
      {
         "index": {
            "_index": "test1",
            "_type": "user3",
            "_id": "1",
            "_version": 1,
            "status": 201
         }
      },
      {
         "index": {
            "_index": "test1",
            "_type": "user3",
            "_id": "2",
            "_version": 1,
            "status": 201
         }
      }
   ]
}
```