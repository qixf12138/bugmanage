import hashlib
from django.test import TestCase

from utills.projectutills.encrypt import md5


class MD5TestCase(TestCase):

    def test_same_password(self):
        # 测试相同密码进行md5加密
        pwd_a = "abcde"
        pwd_b = "abcde"
        self.assertEqual(md5(pwd_a), md5(pwd_b))

    def test_different_password(self):
        # 测试不同密码进行md5加密
        pwd_a = "abcde"
        pwd_b = "edcba"
        self.assertNotEqual(md5(pwd_a), md5(pwd_b))

    def test_secret_key(self):
        # 测试使用的md5加密方式是否加盐
        pwd_a = "abcde"
        pwd_b = "abcde"
        md5_no_secret_key = hashlib.md5()
        md5_no_secret_key.update(pwd_a.encode("utf-8"))
        md5_no_secret_key_result = md5_no_secret_key.hexdigest()
        self.assertNotEqual(md5_no_secret_key_result, md5(pwd_b))

