title: python第三方包在windows上的安装
date: 2015-09-14 09:45:59
tags: [python]
categorys: [python]
---

## 碰到问题 ##

在window上安装某些用c语言开发的第三方包，需要对第三方包先进行编译，由于缺少编译环境尝尝报错`error: Unable to find vcvarsall.bat`

## 解决方法 ##

1.使用MinGW

+ 安装[MinGW](http://sourceforge.net/projects/mingw/files/ 'MinGW') 或者直接安装[CodeBlocks-MinGW](http://www.codeblocks.org/downloads/binaries 'Code::Blocks')
+ 设置%MinGW_HOME%/bin到环境变量中
+ 复制%MinGW_HOME%/bin/mingw32-make.exe为make.exe
+ 在安装python第三方包时使用`python setup.py install build --compiler=mingw32`

2.使用VS

对于已经安装vs的同学只需要在运行`python setup.py install`之前修改环境变量VS90COMNTOOLS为安装vs版本对应的COMNTOOLS路径即可

+ vs2015: `set VS90COMNTOOLS=%VS140COMNTOOLS%`
+ vs2013: `set VS90COMNTOOLS=%VS120COMNTOOLS%`
+ vs2012: `set VS90COMNTOOLS=%VS110COMNTOOLS%`
+ vs2010: `set VS90COMNTOOLS=%VS100COMNTOOLS%`
    
