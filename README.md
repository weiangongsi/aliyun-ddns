# 阿里云ddns-python脚本

##### 配置文件

```yaml
access_key_id: "LTAIPa******"
access_key_secret: "xwnEsyZcjzpJc*******"
wait_sync_time: 1200 # 多少秒强制同步一次,(强制同步是防止网络闪断又重连后时间太短，ping任务此时阻塞等待下一次ping，检测不到网络变化)
wait_listen_time: 5 # 多少秒ping一次检测网络是否正常，如果检测到网络断开，就开始实时检测网络状态，网络正常后立即同步
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
