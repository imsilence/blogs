title: django 后台管理
date: 2015-05-26 21:18:21
tags: [django, python]
categories: [web]
---

## 创建后台管理员 ##

`python manage.py createsuperuser`

## 登录后台 ##

访问`http://localhost:43001/admin`

## 添加自己的模块到后台管理 ##

在blogs/blogsplatform/admin.py中添加注册

```
from django.contrib import admin

# Register your models here.
from .models import Category, Blog

class BlogStackedInline(admin.StackedInline):
    model = Blog
    extra = 3

class BlogTabularInline(admin.TabularInline):
    model = Blog
    extra = 1
    pass

class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name', 'create_date']
    inlines = [BlogTabularInline]

    list_display = ('category_name', 'create_date')

class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['blog_title', 'blog_content', 'category']}),
        ('Date Information', {'fields': ['create_date'], 'classes':['collapse']}),
    ]

    list_display = ('blog_title', 'blog_content', 'create_date', 'was_created_recently')
    list_filter = ['create_date']
    search_fields = ['blog_title', 'blog_content']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
```

+ 自定义django admin表单

使用在ModelAdmin中使用方fields指定在表单中显示的表单项

可以使用fieldsets将表单项进行分组

在存在内联关系时，可在被关联的ModelAdmin中使用inlines关联显示其他表的信息

+ 自定义django admin列表

使用list_display控制列表显示列信息

使用list_filter控制过来条件

使用search_fileds指定查询条件