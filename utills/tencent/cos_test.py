import sys
import os
import logging

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from utills.projectutills.randomobj import create_random_str
from utills.projectutills.tools import get_now_data_str


# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
# 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。
# 子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_id = 'AKIDe7JF2aspWx84lCMHwMYUqxoOghSw96mC'
# 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。
# 子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_key = 'C2dy3qNehTyEEx6zd3FAqFNEpBHsELDq'

region = 'ap-beijing'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

bucket_str = create_random_str(16).lower() + "-" + "1318476280"
print(bucket_str)
response = client.create_bucket(
    Bucket=bucket_str,
)

#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
# response = client.upload_file(
#     Bucket='qixf-1318476280',
#     LocalFilePath="1.jpg",
#
#     Key='1123.jpg',
#     PartSize=1,
#     MAXThread=10,
#     EnableMD5=False
# )
# print(response['ETag'])

# 查询对象列表
# response = client.list_objects(
#     Bucket='qixf-1318476280',
#     Prefix='folder1'
# )
# print(response)

# ####  获取文件到本地
# response = client.get_object(
#     Bucket='qixf-1318476280',
#     Key='1.jpg',
# )
# response['Body'].get_stream_to_file('output.txt')
#
# #### 获取文件流
# response = client.get_object(
#     Bucket='qixf-1318476280',
#     Key='1.jpg',
# )
# fp = response['Body'].get_raw_stream()
# print(fp.read(2))
#
# #### 设置 Response HTTP 头部
# response = client.get_object(
#     Bucket='qixf-1318476280',
#     Key='1.jpg',
#     ResponseContentType='text/html; charset=utf-8'
# )
# print(response['Content-Type'])
# fp = response['Body'].get_raw_stream()
# print(fp.read(2))

# 删除object
## deleteObject
# response = client.delete_object(
#     Bucket='qixf-1318476280',
#     Key='1123.jpg'
# )
# print(response)
