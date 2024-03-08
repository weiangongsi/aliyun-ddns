#!/usr/bin/python
import time
import logging
import requests
import yaml
from alibabacloud_alidns20150109 import models as alidns_models
from alibabacloud_alidns20150109.client import Client as AlidnsClient
from alibabacloud_tea_openapi import models as open_api_models

logging.basicConfig(level=logging.INFO)


class UpdateDns:

    def __init__(self):
        pass

    @staticmethod
    def get_ip():
        html_data = requests.get("http://api.ipify.org?format=json")
        return html_data.json()["ip"]

    @staticmethod
    def get_properties():
        with open("properties.yaml", encoding="utf-8") as file:
            content = file.read()
            return yaml.full_load(content)

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> AlidnsClient:
        config = open_api_models.Config(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )
        config.endpoint = f"alidns.cn-hangzhou.aliyuncs.com"
        return AlidnsClient(config)

    @staticmethod
    def add_domain_record(
        client: AlidnsClient,
        domain_name: str,
        rr: str,
        type: str,
        value: str,
    ) -> AlidnsClient:
        request = alidns_models.AddDomainRecordRequest()
        request.domain_name = domain_name
        request.rr = rr
        request.type = type
        request.value = value
        client.add_domain_record(request)

    @staticmethod
    def update_domain_record(
        client: AlidnsClient,
        record_id: str,
        rr: str,
        type: str,
        value: str,
    ) -> AlidnsClient:
        request = alidns_models.UpdateDomainRecordRequest()
        request.record_id = record_id
        request.rr = rr
        request.type = type
        request.value = value
        client.update_domain_record(request)


if __name__ == "__main__":
    pro = UpdateDns.get_properties()
    domain_list = pro["domain_list"]
    access_key_id = pro["access_key_id"]
    access_key_secret = pro["access_key_secret"]
    wait_seconds_time = pro["wait_seconds_time"]
    client = UpdateDns.create_client(access_key_id, access_key_secret)
    while True:
        try:
            for domain_item in domain_list:
                # 参数
                domain_name = domain_item["domain_name"]
                rr = domain_item["rr"]
                type = "A"
                sub_domain = rr + "." + domain_name
                # 查询子域名A记录
                request = alidns_models.DescribeSubDomainRecordsRequest()
                request.sub_domain = sub_domain
                request.type = type
                records = client.describe_sub_domain_records(request)
                body = records.body
                total_count = body.total_count
                domain_records = body.domain_records
                ip = UpdateDns.get_ip()
                # 查询结果判断
                if total_count == 0:
                    logging.info(sub_domain + ":add_domain_record::" + ip)
                    UpdateDns.add_domain_record(client, domain_name, rr, type, ip)
                else:
                    domain = domain_records.record[0]
                    value = domain.value
                    if value != ip:
                        logging.info(sub_domain + ":update_domain_record::" + ip)
                        record_id = domain.record_id
                        UpdateDns.update_domain_record(client, record_id, rr, type, ip)
                    else:
                        logging.info(sub_domain + ":no change")
        except Exception as e:
            logging.error(e)
        finally:
            time.sleep(wait_seconds_time)