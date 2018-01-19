title: django package制作
date: 2015-05-26 23:18:21
tags: [django, python]
categories: [web]
---

+ 创建django-app(django-blogs)目录,目录下包含项目开发的app(blogsplatform)的所有代码(`cp -r blogs/blogsplatform django-blogs`)

+ 创建README.md文档  

```
# Blogs #

Blogs是一个练习django的项目，用来自己博客的管理和查看

Quick Start
----------
1.install app

`pip install blogs`


2.add "blogsplatform" to your INSTALLED_APPS

INSTALLED_APPS = (
    ...,
    'blogsplatform',
)
3.incloud the blogsplatform URLconf in your project urls.py

urlpatterns = [
    ...,
    url(r'^platform/', include('blogsplatform.urls', namespace='blogsplatform')),
]

4.create the models

`python manage.py makemigrations blogsplatfrom`

`python manage.py migrate`

5.run server

`python manage runserver 0.0.0.0:8080`

6.create super user

`python manage.py createsuperuser`

7.visit http://localhost:8080/admin/

8.visit http://localhost:43001/platform/categorylist/

```

+ 添加证书

创建LICENSE目录，添加证书信息

+ 编写setup.py

```
import os
from setuptools import setup

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CURR_PATH, 'README.md'), 'r') as readme:
    README = readme.read()

setup(
    name='django-blogs',
    version='0.1',
    packages=['blogsplatform'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to blogs',
    long_description=README,
    author='Silence',
    author_email='imsilence@outlook.com',
    classifiers=[
    ],
)
```

+ 创建MANIFEST.in文档

    用于在生成package包时将LICENSE， README.md等信息打入到package中
    
    文件内容如下:
    
```
include LICENSE
include README.md
recursive-include blogsplatform/static *
recursive-include blogsplatform/templates *                               
```

+ 生成tar.gz

`python setup.py sdist`

+ 安装

`pip install django-blogs-0.1.tar.gz`

+ 卸载

`pip uninstall django-blogs`
