import random
import datetime
import inspect
from django_redis import get_redis_connection


# 生成验证码,并根据session加入到redis
def generate_code(mobile_phone, ex_time=60*5):
    # redis 连接测试
    code = str(random.randrange(100000, 999999))
    conn = get_redis_connection("default")
    conn.set(mobile_phone, code, ex=ex_time)

    return code


# 验证手机验证码是否正确
def valid_code(mobile_phone, code):
    conn = get_redis_connection("default")
    if conn.get(mobile_phone):
        redis_code = conn.get(mobile_phone).decode("utf-8")
    else:
        return False
    return redis_code == code


# 查看IP是否已被限制，没有限制返回False
# 如果以没有限制，将IP地址加入到redis中,有效期60秒，返回True
def ip_is_limit(request, ex_time=10):
    user_ip = request.META.get("REMOTE_ADDR")
    conn = get_redis_connection("default")
    ip_status = conn.get(user_ip)
    if ip_status:
        print(ip_status)
        return True
    conn.set(user_ip, 1, ex=ex_time)
    return False


# 获取当前时间字符串
def get_now_data_str(str_format="%Y-%m-%d %H:%M:%S"):
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime(str_format)
    return now_time_str


# 获取一个类所有的类名
def get_class_names(module):
    # 创建一个空列表，用来存储类名
    class_names = []
    # 遍历模块中的所有对象
    for name in dir(module):
        # 获取对象的引用
        obj = getattr(module, name)
        # 判断对象是否是类
        if inspect.isclass(obj):
            # 获取类的名称，并添加到列表中
            class_names.append(obj.__name__)
    # 返回列表
    return class_names