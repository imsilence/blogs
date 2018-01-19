title: windows服务注册
date: 2015-08-12 21:29:17
tags: [windows service registe]
categories: [软件安装]
---
## 简介 ##

  在很多情况下需要应用程序随系统启动而在后台运行，例如在widows环境中运行nginx或者kafka，应用程序并未提供服务注册功能，此时需要借助于其他工具。以下介绍使用Windows Server 2003 Resource Kit Tools中的instsrv.exe和srvany.exe将应用程序注册到windows服务当中。
  
  instsrv.exe为服务注册工具
  srvany.exe为注册程序的服务外壳

## 程序获取 ##

[下载](http://www.microsoft.com/en-us/download/details.aspx?id=17657 rktools)并安装rktooks，在安装目录拷贝instsrv.exe和srvany.exe到C:\Windows\System32目录（注：在x64系统下同时需要拷贝到C:\Windows\SysWOW64目录）

直接从网盘[下载](http://yunpan.cn/cdMBBYiEyvUHL) instsrv.exe和srvany.exe程序，提取码为: 90c6

## 使用方法 ##

+ 安装服务

  1.注册服务
    使用系统管理员权限在命令行中执行：`instsrv ServerName "C:\\Windows\\System32\\srvany.exe"`
    说明：ServerName为服务名称
  
  2.修改注册表内容
    a.在路径HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Services/ServerName下新建项Parameters
    b.在Parameters下新建字符串值Application, AppDirectory,AppParameters
      说明：Application值设置为应用程序的绝对路径
            AppDirectory值设置为应用程序所在目录
            AppParameters值设置为应用程参数
      
      例如,设置kafka服务：
          Application="C:\ProgramFiles\kafka\bin\windows"
          AppDirectory="C:\ProgramFiles\kafka\bin\windows\kafka-server-start.bat"
          AppParameters="C:\ProgramFiles\kafka\config\server-9092.properties"

+ 启动服务
  
  使用系统管理员权限在命令行中执行：`net start ServerName`

+ 停止服务

  使用系统管理员权限在命令行中执行：`net stop ServerName`
  
  注意：在很多情况下使用net stop并不能杀死服务运行的子进程，需要使用`TASKKILL /F /IM image.exe /T` kill掉进程

+ 删除服务

  使用系统管理员权限在命令行中执行：`instsrv ServerName remove`