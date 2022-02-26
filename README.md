# 阿里云ddns-python脚本

##### 配置文件

```yaml
access_key_id: "LTAIPa******"
access_key_secret: "xwnEsyZcjzpJc*******"
wait_seconds_time: 30 # 多少秒同步一次
domain_list: # 域名列表
  - rr: www # 记录值
    domain_name: dcssn.com # 域名
  - rr: ftp
    domain_name: dcssn.com
```

##### 安装依赖

```
pip instsall -r requirements.txt
```

##### 运行

```
python ddns.py
```
docker
```
docker build -t aliyun-ddns .
docker run -d --name=aliyun-ddns --restart=always  aliyun-ddns
```
