title: nginx配置ssl双向证书
date: 2016-11-09 09:40:21
tags: [nginx, ssl]
categories: [server]
---

# CA根证书制作 #

```
# 创建CA私钥
open genrsa -out ca.key 2048

#制作CA根证书(公钥)
openssl req -new -x509 -days3650 -key ca.key -out ca.crt
```

# 制作证书 #

```
# 创建私钥
openssl genrsa -out server.pem 1024
openssl rsa -in server.pem -out server.key

# 生成签发请求
openssl req -new -key server.pem -out server.csr

# 使用CA证书进行签发
openssl x509 -req -sha256 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 -out server.crt

# 制作p12证书(导入浏览器)
openssl pkcs12 -export -clcerts -in server.crt -inkey server.key -out server.p12
```

客户端证书创建方式与服务器证书创建方式相同

# nginx配置 #

```
ssl on;
ssl_certificate ssl/server.crt;
ssl_certificate_key ssl/server.key;
ssl_client_certificate ssl/ca.crt;
ssl_verify_client on;
```

# 使用 #
```
curl --key client.key --cert client.crt -XGET "https://localhost:11443" -k -v
