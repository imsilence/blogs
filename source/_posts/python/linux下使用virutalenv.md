title: linux下使用virtualenv
date: 2016-02-18 01:20:21
tags: [virtualenv, liniux]
categories: [工具]
---

## virtualenv使用 ##

1. 安装
`pip install virtualenv`

2. 配置
vi ~/.bashrc

`export VIRTUALENV_USE_DISTRIBUTE=true`

## virtualenvwrapper使用 ##

1. 安装
`pip install virtualenvwrapper`

2. 指定virtualenvwrapper虚拟环境默认路径
vi ~/.bashrc

```
# config virtualenvwrapper
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
  export WORKON_HOME=$HOME/.virtualenvs
  source /usr/local/bin/virtualenvwrapper.sh
fi
```

3. 创建虚拟环境
`mkvirtualenv env`

4. 查看所有虚拟环境和启动虚拟环境
`lsvirtualenv`
`workon`
`workon env`

5. 退出虚拟环境
`deactivate`