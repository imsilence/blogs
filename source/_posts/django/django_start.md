title: Django 启动
date: 2015-05-26 18:18:21
tags: [django, python]
categories: [web]
---

## 创建项目 ##

`django-admin.py startproject blogs`

项目目录结构：
```
blogs
├── blogs
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

说明:

+ manage.py:django命令行工具
+ settings.py:项目设置
+ urls.py:项目url配置
+ wsgi.py:项目web访问入口

## 数据库配置 ##

+ 配置文件:blogs/blogs/settings.py

DATABASES 属性用户配置项目使用的数据库，可配置多个:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mysql': {
        'ENGINE'： 'django.db.backends.mysql',
        'NAME'： 'blogs',
        'USER'： 'user',
        'PASSWORD'： 'pwd',
        'HOST'： 'localhost',
        'PORT'：3306
    }
}
```

数据库配置说明：

ENGINE: 用于指定数据库驱动
NAME： 数据库名称，若使用sqlite则为sqlite文件路径
USER： 数据库连接用户名
PASSWORD： 数据库连接密码
HOST： 数据库连接主机地址
PORT： 数据库连接端口号

+ 数据库逆向创建

若使用非sqlite数据库，则需要在逆向创建数据表前使用`CREATE DATABASE dbname`创建数据库,然后在使用`python manage.py migrate`逆向创建数据表

## 启动服务 ##

`python manage.py runserver 0.0.0.0:43001`

## 创建应用 ##

+ 初始化应用

`python manage.py startapp blogsplatform`

目录结构如下：
```
blogsplatform/
├── admin.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.p
```

+ 添加应用到项目中

在blogs/blogs/setting.py的INSTALLED_APPS属性中添加创建的应用名称
```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogsplatform',
)
```

+ 创建 models

在blogsplatform/models.py中编辑文件创建db操作类

```
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=250)
    create_date = models.DateTimeField('date created')

    def __unicode__(self):
        return '%s:%s:%s' % (self.id, self.category_name, self.create_date)


class Blog(models.Model):
    blog_content = models.TextField()
    create_date = models.DateTimeField('date created')
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return '%s:%s:%s:%s' % (self.id, self.category.category_name, self.blog_content, self.create_date)

```

+ 同步数据库

生成migrations文件，用于通知django自己的model发生的变化

`python manage.py makemigrations blogsplatform`

查看sql语句

`python manage.py sqlmigrate blogsplatform 0001

同步数据库表

`python manage.py migrate`

## django shell ##

django shell是django操作的一个命令行接口，启动时已初始化django环境

`python manage.py shell`

操作如下：
```
In [1]: from blogsplatform.models import Category, Blog

In [2]: from django.utils import timezone

In [3]: category = Category(category_name='生活随笔', create_time=timezone.now())

In [4]: category = Category(category_name='生活随笔', create_date=timezone.now())

In [5]: category.save()

In [6]: Category.objects.all()

Out[6]: [&lt;Category: 1:生活随笔:2015-05-26 01:05:21.191538+00:00&gt;]

In [8]: category.blog_set.all()

Out[8]: []

In [9]: blog = category.blog_set.create(blog_content='test', create_date=timezone.now())

In [17]: Blog.objects.count()

Out[17]: 1

In [18]: blog.blog_content

Out[18]: 'test'

In [19]: blog.blog_content = 'test1'

In [20]: Blog.objects.all()

Out[20]: [&lt;Blog: 1:生活随笔:test:2015-05-26 01:09:07.316380+00:00&gt;]

In [21]: blog.save()

In [22]: Blog.objects.all()

Out[22]: [&lt;Blog: 1:生活随笔:test1:2015-05-26 01:09:07.316380+00:00&gt;]

In [23]: blog2 = Blog(blog_content='test2', create_date=timezone.now(), category=category)

In [24]: blog2.save()

In [25]: Blog.objects.filter(pk=2)
Out[25]: [&lt;Blog: 2:生活随笔:test2:2015-05-26 01:16:24.733357+00:00&gt;]

In [26]: category.blog_set.count()
Out[26]: 2

In [27]: tblog2 = category.blog_set.get(pk=2)

In [28]: tblog2.delete()

In [29]: Blog.objects.get(pk=2)

In [31]: Blog.objects.filter(blog_content__startswith='test')

Out[31]: [&lt;Blog: 1:生活随笔:test1:2015-05-26 01:09:07.316380+00:00&gt;]
```