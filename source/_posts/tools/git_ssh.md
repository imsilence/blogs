title: git ssh使用
date: 2015-10-16 12:15:21
tags: [git]
categories: [工具]
---

访问git仓库可以使用sshkey的方式，首先需要生成key

使用ssh-agent配置公私钥，windows下需要安装[Github for Windows](https://desktop.github.com/) 或者 [msysgit](https://git-for-windows.github.io/)

1.生成公、私钥
```
ssh-keygen -t rsa -b 4096 -C "Silence"
```
2.添加私钥到ssh-agent

```
ssh-agent -s
#若启动失败可以使用
eval $(ssh-agent -s)

ssh-add ~/.ssh/id_rsa
```

3.添加公钥到git server
