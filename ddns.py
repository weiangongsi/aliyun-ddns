#!/usr/bin/python

import time

import requests
import yaml
from alibabacloud_alidns20150109 import models as alidns_models
from alibabacloud_alidns20150109.client import Client as AlidnsClient
from alibabacloud_tea_openapi import models as open_api_models
from lxml import etree


class UpdateDns:

    def __init__(self):
        pass

    @staticmethod
    def create_client(access_key_id: str, access_key_secret: str, ) -> AlidnsClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return AlidnsClient(config)

    @staticmethod
    def main() -> None:
        print('开始执行')
        pro = UpdateDns.get_properties()
        access_key_id = pro['access_key_id']
        access_key_secret = pro['access_key_secret']
        wait_seconds_time = pro['wait_seconds_time']
        client = UpdateDns.create_client(access_key_id, access_key_secret)
        domain_list = pro['domain_list']
        for domain_item in domain_list:
            describe_sub_domain_records_request = alidns_models.DescribeSubDomainRecordsRequest()
            describe_sub_domain_records_request.sub_domain = domain_item['rr'] + '.' + domain_item['domain_name']
            describe_sub_domain_records_request.type = 'A'
            # 复制代码运行请自行打印 API 的返回值
            records = client.describe_sub_domain_records(
                describe_sub_domain_records_request)
            body = records.body
            total_count = body.total_count
            domain_records = body.domain_records
            ip = UpdateDns.get_ip()
            if total_count == 0:
                print(domain_item, '没有记录，新增记录', ip)
                add_domain_record_request = alidns_models.AddDomainRecordRequest()
                add_domain_record_request.domain_name = domain_item['domain_name']
                add_domain_record_request.rr = domain_item['rr']
                add_domain_record_request.type = 'A'
                add_domain_record_request.value = ip
                result = client.add_domain_record(add_domain_record_request)
                print(domain_item, '新增结果', result.body)
            else:
                domain = domain_records.record[0]
                value = domain.value
                if value != ip:
                    print('记录存在', domain, '，值不同，需要更新', ip)
                    update_domain_record_request = alidns_models.UpdateDomainRecordRequest()
                    update_domain_record_request.record_id = domain.record_id
                    update_domain_record_request.rr = domain_item['rr']
                    update_domain_record_request.type = 'A'
                    update_domain_record_request.value = ip
                    result = client.update_domain_record(update_domain_record_request)
                    print(domain_item, '更新结果', result.body)
                else:
                    print(domain, '记录存在，不需要更新')
        print('等待', wait_seconds_time, '秒')
        time.sleep(wait_seconds_time)

    @staticmethod
    def get_ip():
        html_data = requests.get(
            'http://www.net.cn/static/customercare/yourip.asp')
        tree = etree.HTML(html_data.text)
        ip = tree.xpath('//h2')
        return ip[0].text.strip()

    @staticmethod
    def get_properties():
        with open('properties.yaml', encoding="utf-8") as file:
            content = file.read()
            return yaml.full_load(content)


if __name__ == '__main__':
    while True:
        UpdateDns.main()
