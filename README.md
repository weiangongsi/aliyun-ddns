# 阿里云ddns-python脚本

只支持ipv4，如果有别的需求可以提出来加上。

##### 配置文件

```yaml
access_key_id: "LTAIPa******"
access_key_secret: "xwnEsyZcjzpJc*******"
wait_seconds_time: 30 # 多少秒同步一次，阿里云查询域名解析API配额速率为：300/1(s)，无需担心接口调用次数问题
domain_list: # 域名列表
  - rr: www # 记录值
    domain_name: dcssn.com # 域名
  - rr: ftp
    domain_name: dcssn.com
```

##### 运行

```
pip instsall -r requirements.txt
python ddns.py
```
##### docker
```
docker build -t aliyun-ddns .
docker run -d --name=aliyun-ddns  aliyun-ddns
```
