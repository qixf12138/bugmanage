import random

from django_redis import get_redis_connection
from django_redis.exceptions import ConnectionInterrupted


def generate_code(mobile_phone, ex_time=60*5):
    # 生成验证码,并根据session加入到redis
    # redis 连接测试
    code = str(random.randrange(100000, 999999))
    conn = get_redis_connection("default")
    conn.set(mobile_phone, code, ex=ex_time)

    return code


def valid_code(mobile_phone, code):
    # 验证手机验证码是否正确
    conn = get_redis_connection("default")
    if conn.get(mobile_phone):
        redis_code = conn.get(mobile_phone).decode("utf-8")
    else:
        return False
    return redis_code == code





