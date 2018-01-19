title: GO安装&运行
date: 2015-09-20 11:18:21
tags: [golang]
categories: [开发语言]
---

## 环境搭建 ##

+ windows x64
1. 下载安装包, x64安装包戳这里[下载](http://yunpan.cn/cHZSFU6mehsua 'go windows x64 安装程序'), 提取码为: ce54
2. 安装程序
3. 设置环境变量, 新建变量GOROOT为GO的安装目录, 将%GOROOT%\bin添加到Path中
4. 打开新cmd, 输入: `go version`, 查看go版本号验证程序和配置OK 

+ ubuntu
1. 使用apt命令进行安装: `sudo apt-get install golang`
2. 在/etc/environment中配置环境变量
```
export GOROOT=GO_HOME
export PATH=$GOROOT\bin;$PATH
```

说明: 
1. 配置完成后使用`source /etc/environment`使配置文件生效
2. 使用apt-get等工具在linux上安装go后, 会自动将go的执行程序拷贝到/usr/bin/下, 因此一般不许要配置环境

## 示例 ##
```
#file: main.go
package main

import "fmt"
func main() {
    fmt.Println("Hello, World!")
}

```

运行程序: `go run helloworld.go`
编译&运行程序: `go build hellowrold.go && helloworld.exe`

说明:
1. go程序的入口为package为main的main方法
2. 在相同的目录下go文件package必须相同, 若以目录为单位编译&运行项目, 则在编译目录下的所有go文件中的package名称必须为main且只能有一个main函数
使用: `cd pk_dir && go run ./pk_name`
3. 在项目编译或运行时若使用main以外的package, 则package所在目录或其父目录必须设置的环境变量GOPATH中
若想要在非pk_dir运行`go run pk_name`进行运行目录的项目, 则pk_dir目录或其父目录必须在GOPATH中
