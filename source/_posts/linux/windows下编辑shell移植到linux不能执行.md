title: windows下编辑shell移植到linux后不能执行
date: 2015-09-22 11:20:21
tags: [shell]
categories: [linux]
---

## 背景 ##
在linux下编辑了shell文件后移植到linux后报错: `-bash: ./test.sh: /bin/sh^M: bad interpreter: No such file or director`

## 解决方法 ##
1. 在linux下使用vi打开文件
2. 查看文件格式: `:set ff` 显示: `ff=doc`
3. 设置文件个格式: `:set ff=unix`

现在执行应该就ok了