title: HTTP
date: 2015-07-25 23:18:21
tags: [http]
categories: [web]
---

## 简介 ##

HTTP(HyperText Transfer Protocol, 超文本传输协议) 是访问互联网使用的核心通信协议，也是所有web应用程序使用的通信协议。
消息模型：客户端发送请求消息，服务器返回响应消息。传输层使用具有状态的TCP协议，但HTTP协议本身不具有状态。

## HTTP请求 ##

HTTP请求消息分为消息头和消息主体（可选），消息头和消息主体用空白行分隔。实例：
```
GET / HTTP/1.1
Host: www.cnbeta.com
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=&tn=baidu&bar=&wd=cnbeta&rn=&rsv_pq=917ee072000177b3&rsv_t=67c29bDcYXbklwxp5LMXvSvgQrSWnKznmk4XgHbAghkt7XqGt%2BfEuP%2BMDo4
Cookie: Hm_lvt_4216c57ef1855492a9281acd553f8a6e=1437836998; Hm_lpvt_4216c57ef1855492a9281acd553f8a6e=1437836998; _ga=GA1.2.1311393193.1437836981; bfd_s=208385984.21594488.1437837000279; tma=208385984.15187292.1437837000282.1437837000282.1437837000282.1; tmd=1.208385984.15187292.1437837000282.; bfd_g=b56c782bcb75035d00000a500201ba8455b3a6ca
Connection: keep-alive


```
说明：
1.消息头第一行由三个以空格分隔的元素组成，分别为HTTP方法、请求的URL和使用的HTTP版本
  + HTTP方法；
    1). GET：用于获取资源，参数通过URL查下字符串方式提交给服务器，无消息主体
    2). POST：用于执行操作，参数可以通过URL查下字符串方式和消息主体提交给服务
    3). HEAD：用于检测资源是否存在，与GET类似，区别在于在响应消息中返回的消息主体为空
    4). TRACE：用于诊断，可判断客户端和服务器之间是否存在代理服务器，原理：服务器在响应主体中返回收到的请求消息的具体内容
    5). OPTIONS：用于要求服务器报告对某一资源有效的HTTP方法，服务器常返回Allow消息头的响应，并列出所有有效的方法
    6). PUT：使用请求主体中的内容向服务器上传指定的资源
    7). DELETE：用于删除资源
    8). CONNECT：

  + 请求URL：用于指定请求的资源名称以及查下参数
  + 使用的HTTP版本：常用1.0和1.1版本，在1.1版本中请求消息中必须包含Host请求头

2.其他
  + Host：指定请求访问的主机名，当多个web站点部署在同一台主机上时需要使用Host消息头
  + User-Agent：指定客户端软件的信息，不如浏览器类型和版本、操作系统类型和版本等
  + Referer：表示发出请求的原始URL
  + Cookie：提交服务器想客户端发布的其他参数

## HTTP 响应 ##

HTTP响应消息分为消息头和消息主体（可选），消息头和消息主体用空白行分隔。实例：
```
HTTP/1.0 200 OK
Content-Type: text/html
Last-Modified: Sat, 25 Jul 2015 15:52:02 GMT
Vary: Accept-Encoding
Server: nginx/1.4.1
Date: Sat, 25 Jul 2015 15:53:04 GMT
ETag: "55b3b0a2-2539c"
Age: 74
X-Cache: HIT from RJ-ZSBGP-CDN-74
Set-Cookie: uuid=AQAAAEx080zNuwoAJH3PdhcuX+oK943s; Path=/; Expires=Sat, 25-Jul-15 17:09:08 GMT; HttpOnly

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>cnBeta.COM</title>

<body>
Hello, Silence!
</body>
</html>
```

说明：

1.消息头第一行由三个空格分开的元素组成，分别表示HTTP版本、请求状态码（数字）、请求状态描述
2.其他：
  + Server：旗标，指明使用的Web服务器软件
  + Set-Cookie：设置cookie信息，在随后向服务器发送的请求中由Cookie消息头返回
  + Content-Type：指定消息主体类型
  + Content-Length:指定消息主体的字节长度

## URL ##

URL(Uniform Resource Locator，统一资源定位符)是web资源的唯一标识，格式：

`
protocol://hostname[:port]/[path/]file[?param=value]
`

## REST ##

REST(表达性状态转移)是分布式系统的一个体系架构，REST风格URL 指在URL中使用文件路径方式替代查询字符串

## HTTP消息头 ##

1.常用消息头
  + Connection：用于指定告诉通信另一端传输完成后关闭TCP连接还是保持连接，HTTP/1.1中默认为keep-alive，可设置为close
  + Content-Encoding：用于指定消息主体中编码格式
  + Content-Length；用于指定消息主体的字节长度
  + Content-Type：用于指定消息主体的内容类型
  + Transfer-Encoding：常指定为Transfer-Encoding:chunked，用于表示边产生数据边传输，在最后一块数据中`0\r\n\r\n`标识数据结束，在其他块数据中格式为`\r\ncontent\r\n`

2.请求消息头
  + Accept：用于告知服务器客户端接受哪些类型的数据
  + Accept-Encoding：用于告知服务器客户端接受哪些编码格式
  + Authorization：用于内置HTTP身份验证，用于提交用户名/密码给服务器
  + Cookie：提交Cookie
  + If-Modified-Since：用于告知服务器最后一次收到请求资源的响应时间，当资源未发生变化时服务器返回状态码304表示使用本地缓存
  + If-None-Match：用于指定实体标签，说明主体内容的标识符，当最后一次收到所请求的资源时，浏览器提交服务器发布的实体标签。服务器可通过使用实体标签确定浏览器是否使用缓存副本
  + Origin：用在Ajax跨域请求，指定发出请求的域名
  + Referer：指定发出请求额原始URL
  + User-Agent：用于指定客户端信息

3.响应消息头
  + Access-Control-Allow-Origin:用于指顶是否可通过跨域Ajax请求获取资源
  + Cache-Control：用于向浏览器发送缓存指令（no-cache）
  + Etag：指定实体标签，客户端可在后续提交实体标签获得与If-None-Match消息头相同的资源，通知服务器浏览器当前缓存保存的是哪个版本的资源
  + Expires：指定消息主体的有效时间，在时间内，浏览器可使用资源的缓存副本
  + Location：重定向响应，说用重定向的目标
  + Pragma：向浏览器传送缓存指令（no-cache）
  + Server：告知浏览器服务器软件相关信息
  + Set-Cookie：向浏览器发布cookie
  + WWW-Authenticate：用于401状态码响应，提供与服务器所支持的身份验证类型等信息
  + X-Frame-Options：指示浏览器Frame是否及如何加载当前响应

## cookie ##

服务器使用Set-Cookie响应消息头向浏览器发布cookie信息，可以使用多个响应消息头发布多个cookie，浏览器也可使用Cookie请求消息头提交使用分号分隔的多个cookie信息给服务器

cookie具有名称、值、有效时间、有效域、有效路径、是否为https请求、是否可在客户端修改属性，可通过Set-Cookie响应消息头设置，参数列表如下：
+ expires：指定cookie有效时间，若未指定则表示只保存在当前浏览器回话中
+ domain：指定cookie有效域，必须和收到cookie的域相同或者是其父域
+ path：指定cookie的有效url路径
+ secure：仅仅在https请求中提交cookie信息
+ httpOnly：用于指定在客户端是否可以通过js修改cookie信息

## 状态码 ##

状态码用于说明请求结果，分为5大类：
+ 1XX：提供信息
+ 2XX：请求成功
+ 3XX：请求重定向
+ 4XX：请求包含错误
+ 5XX：服务器执行错误

常见状态码说明：
+ 100 Continue：当客户端提交一个包含主体的请求时，将发送该响应，表示已收到请求消息头，客户端继续发送主体
+ 200 OK：请求成功，且响应主体中包含请求结果
+ 201 Created：PUT请求的响应返回状态码，表示请求成功提交
+ 301 Moved Permanently：指示浏览器永久重定向到Location指定的URL，客户端使用新的URL替换原始URL
+ 302 Found：指示浏览器暂时重定向到Location指定的URL，客户端随后的请求恢复到原始URL
+ 304 Not Modified：指示浏览器使用缓存中保存的资源副本
+ 400 Bad Request：表示发起无效HTTP请求
+ 401 Unauthorized：服务器需要进行HTTP身份认证
+ 403 Forbidden：禁止访问请求资源
+ 404 Not Found：表示资源不存在
+ 405 Method Not Allowd：表示URL不支持请求方法
+ 413 Request Entity Too Large：表示请求主体过长，服务器无法处理
+ 413 Request URI Too Long：表示请求URL过长，服务器无法处理
+ 500 Internal Server Error：表示服务器执行遇到错误
+ 503 Service Unavailable：表示服务器运行正常，但无法做出响应

## HTTPS ##

HTTP使用非加密的TCP作为传输机制，缺点在网络适当位置的攻击者能够截获发送内容,HTTPS和HTTP都属于应用层协议，当HTTPS通过安全传输机制-安全套接层（Secure Socket Layer，SSL）传输数据，可保护通过网络传输数据的机密性和完整性

SSL已经由TLS（Transport Layer Security，传输层安全）代替

## HTTP代理 ##

代理服务器运行在客户端浏览器和web服务器之间，浏览器将所有请求提交给代理服务器，代理服务器将请求传送给相关web服务器，并将响应返回给浏览器

HTTP代理服务器工作机制：
+ 当浏览器向代理服务器发送HTTP请求时，代理服务器将完整URL插入请求中，代理服务器将提取主机名和端口，并使用这些信息将请求指向正确的目标web服务器
+ 当浏览器向代理服务器发送HTTPS请求时，浏览器将代理作为TCP级中继，浏览器使用CONNECT方法向代理服务器提交一个HTTP请求，并指定URL中的目标主机名称和端口号，从而建立中继。若代理允许该请求，则返回200状态码的HTTP响应，一直开放TCP链接，从此以后作为目标web服务器的TCP级中继


## HTTP身份认证 ##

HTTP具有自己的用户身份验证机制，主要方案由：
+ Basic：在请求消息头中随每条消息以Base64编码字符串的形式发送用户证书
+ NTLM：是质询-响应式机制，使用Windows NTLM协议版本
+ Digest：是质询-响应式机制，随同用户证书一起使用一个随机值的MD5校验和