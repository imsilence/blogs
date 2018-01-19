title: bpmappers库
date: 2015-05-27 23:18:21
tags: [python, bpmappers]
categories: [python]
---

## 简介 ##

bpmappers库是将python对象转化为字典类型的库, 在对外提供数据服务类型的功能开发用途较大，尤其后台使用django开发，bpmappers库简便将对象转化为dict类型，配和json.dumps功能对外提供json格式数据

## 安装 ##

`pip install bpmappers`


## 使用 ##

+ 类中属性为的基本类型

类的定义:

```
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

from bpmappers import Mapper, RawField

class PersonMapper(Mapper):
    name = RawField('name')
    age = RawField('age')
```

试验:

```
In [6]: me = Person('silence', 28)

In [7]: PersonMapper(me).as_dict()
Out[7]: {'age': 28, 'name': 'silence'}
```

+ 类中属性存在其他对象进行组合

```
class Blog(object):
    def __init__(self, content, author):
        self.content = content
        self.author = author
        
from bpmappers import DelegateField

class BlogMapper(Mapper):
    content = RawField('content')
    author = DelegateField(PersonMapper, 'author')
```

试验:

```
In [27]: blog = Blog('bpmappers test', me)

In [28]: BlogMapper(blog).as_dict()
Out[28]: {'content': 'bpmappers test', 'author': {'age': 28, 'name': 'silence'}}
```

+ 类属性存在由其他对象组成的列表

```
from bpmappers import ListDelegateField

class Group(object):
    def __init__(self, name, members):
        self.name = name
        self.members = members        

class GroupMapper(Mapper):
    name = RawField('name')
    members = ListDelegateField(PersonMapper, 'members')
```

试验:

```
In [34]: group = Group('python', [me])

In [35]: GroupMapper(group).as_dict()
Out[35]: {'name': 'python', 'members': [{'age': 28, 'name': 'silence'}]}
```

+ 需要将列表或者基本类型进行加上key并转化dict

```

from bpmappers import NonKeyField, NonKeyDelegateField, NonKeyListDelegateField

class ValueMapper(Mapper):
    value = NonKeyField()
    def filter_value(self):
        return str(self.data)

class ValueDelegateMapper(Mapper):
    value = NonKeyDelegateField()
    def filter_value(self):
        return self.data

class ValueListDelegateMapper(Mapper):
    value = NonKeyListDelegateField(PersonMapper)
    def filter_value(self):
        return self.data

```

试验:

```
In [45]: ValueMapper(1).as_dict()
Out[45]: {'value': '1'}

In [46]: ValueMapper([1]).as_dict()
Out[46]: {'value': '[1]'}

In [57]: ValueDelegateMapper(me).as_dict()
Out[57]: {'value': {'age': 28, 'name': 'silence'}}


In [61]: ValueListDelegateMapper([me]).as_dict()
Out[61]: {'value': [{'age': 28, 'name': 'silence'}]}
```

+ callback & after_callback & filter & after_filter & key_name

```
class Value(object):
    def __init__(self, value):
        self.value = value


class ValueMapper(Mapper):
    value = RawField('value',\
                        callback=lambda x:'(cb %s)' % x,\
                        after_callback=lambda x:'[after cb %s]' % x)
    
    def filter_value(self, value):
        return '&lt;filter %s&gt;' % value
        
    def after_filter_value(self, value):
        return '{after_filter %s}' % value
        
    def key_name(self, name, value, field):
        return 'namespace:%s' % name
```

试验:

```
In [77]: ValueMapper(Value('test')).as_dict()
Out[77]: {'namespace:value': '{after_filter [after cb (cb &lt;filter test&gt;)]}'}
```

执行顺序:
1.filter
2.callback
3.after_callback
4.after_filter


+ django model转化

```
from bpmappers import djangomodel

class PersonModelMapper(djangomodel.ModelMapper):
    class Meta:
        model=Person
        exclude=['id']
```

试验:

```
In [77]: PersonModelMapper(Person.objects.get(pk=1)).as_dict()
```
