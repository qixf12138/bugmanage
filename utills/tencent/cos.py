import sys
import os
import logging

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from bugmanage import settings
from utills.projectutills.randomobj import create_random_str


class COSBucket():
    def __init__(self):
        # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        # 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
        # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。
        # 子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.secret_id = settings.secretId
        # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。
        # 子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.secret_key = settings.secretKey

        # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
        self.region = 'ap-beijing'
        # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
        # self.token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
        self.scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.client = CosS3Client(self.config)

    # 创建桶
    def create_bucket(self):
        bucket_str = create_random_str(16).lower() + "-1318476280"
        self.client.create_bucket(Bucket=bucket_str)
        return bucket_str

    # 上传文件
    def upload_file_by_filepath(self, local_filepath, key, bucket, part_size=1, max_thread=10, enable_md5=False):
        response = self.client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_filepath,
            Key=key,
            PartSize=part_size,
            MAXThread=max_thread,
            EnableMD5=enable_md5
        )
        return response['ETag']

    # buffer上传文件
    def upload_file_by_buffer(self, bucket, key, body):
        response = self.client.upload_file_from_buffer(bucket, key, body)
        return response

    # 查询对象列表
    def list_object(self, bucket, prefix=""):
        response = self.client.list_objects(
            Bucket=bucket,
            Prefix=prefix
        )
        return response

    # 获取文件流
    def get_object(self, key, bucket):
        response = self.client.get_object(
            Bucket=bucket,
            Key=key,
        )
        fp = response['Body'].get_raw_stream()
        return fp.read(2)

    # 删除object
    def delete_object(self, key, bucket):
        # deleteObject
        response = self.client.delete_object(
            Bucket=bucket,
            Key=key,
        )
        print(response)



