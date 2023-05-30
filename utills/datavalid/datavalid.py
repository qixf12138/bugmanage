"""
验证数据格式是否正确
"""
import re


def mobilephone_number_vaild(phone_number):
    ret = re.match(r"^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$", phone_number)
    if ret:
        return True
    else:
        return False
