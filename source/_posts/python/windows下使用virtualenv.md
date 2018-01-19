title: windows下使用virtualenv
date: 2015-10-22 10:20:21
tags: [virtualenv, windows]
categories: [python]
---

virtualenv使用：
1. 安装
    `pip install virtualenv`

2. 创建虚拟环境
    `virtualenv env`

3. 启动虚拟环境
    `.\env\Scripts\activate.bat`

4. 查看虚拟环境安装的python包
    `pip install package`
    `easy_install package[.exe|.egg]`

5. 退出虚拟环境
    `deactivate`


在windows上也提供了virtualenvwrapper
1. 安装
    `pip install virtualenvwrapper-win`
    可设置环境变量WORKON_HOME指定virtualenvwrapper虚拟环境默认路径

2. 创建虚拟环境
    `mkvirtualenv env`

3. 查看所有虚拟环境和启动虚拟环境
    `lsvirtualenv`
    `workon`
    `workon env`

4. 退出虚拟环境
    `deactivate`

5. 将指定路径添加到sitepackages目录下的virtualenv_path_extensions.pth中可以直接进行import，在启动虚拟环境时则添加到虚拟环境中，在未启动则添加到默认python环境中
    `add2virtualenv path`

6. 其他命令
    cdproject: 切换目录到当前指定的project目录下, 使用前需要使用setprojectdir进行设置
    cdvirtualenv: 切换到当前虚拟环境目录下
    cdsitepackages: 切换到当前虚拟环境的sitepackages下
    lssitepackages： 查看当前虚拟环境的sitepackages目录下的包
    setprojectdir path： 设置project目录
    toggleglobalsitepackages：启用/关闭系统sitepackages
    whereis file：查看文件路径