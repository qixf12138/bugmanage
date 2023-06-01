import random

from django_redis import get_redis_connection


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


def ip_is_limit(request, ex_time=10):
    # 查看IP是否已被限制，没有限制返回False
    # 如果以没有限制，将IP地址加入到redis中,有效期60秒，返回True
    user_ip = request.META.get("REMOTE_ADDR")
    conn = get_redis_connection("default")
    ip_status = conn.get(user_ip)
    if ip_status:
        print(ip_status)
        return True
    conn.set(user_ip, 1, ex=ex_time)
    return False


