title: centos gcc4.8.5编译
date: 2015-09-23 09:40:21
tags: [centos, gcc编译]
categories: [linux]
---

在centos6.7 x64上编译安装mesos 0.24.0时需要使用gcc 4.8以上版本, 此处记录编译方法
1. 通过GCC镜像[下载](https://gcc.gnu.org/mirrors.html "gcc 4.8.5")
2. 解压tar.gz文件: `tar -zvxf gcc-4.8.5.tar.gz` 并cd到解压目录
3. 下载依赖包, 执行脚本: `./contrib/download_prerequisites`
4. 创建编译目录: `mkdir build && cd build`
5. 生成从makefile文件录: `../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib`
6. make程序: `make -j4`
7. 执行测试用例: `make check/test`
8. 安装: `make install`

注意:
在编译过程中可能出现报错: `gnu/stubs.h: No such file or directory`, 需要安装glibc-devel.i686包, 命令: `yum install glibc-devel.i686`
