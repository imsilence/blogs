title: elasticsearch index别名
date: 2015-10-12 10:10:21
tags: [elasticsearch]
categories: [存储]
---

在ES中可以为index设置别名，通过别名对index进行操作
也可以对多个index设置相同别名, 表示在进行query操作时对多有指定的index进行查询, 但此时不能进行get和put操作

```
#获取所有别名
GET _cat/aliases?v

#获取_index_name模式内所有指定别名为_alias_name模式的index
GET /_index_name/_alias|_aliases/_alias_name
_alias和_aliases的区别为若指定为_aliases在查询时若_index未指定满足要求的别名在返回结果中是否包含但aliasese属性为空, 使用_alias时不包含该index

#设置别名
PUT /_index_name/_alias/_alias_name

#删除别名
DELETE /_index_name/_alias/_alias_name

```