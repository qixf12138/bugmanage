from django.test import TestCase
from user.models import UserInfo


class UserInfoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 创建一些测试数据，只在类级别执行一次
        UserInfo.objects.create(user="Alice", password="123456", email="alice@example.com", mobile_phone="13800000000", gender=0)
        UserInfo.objects.create(user="Bob", password="654321", email="bob@example.com", mobile_phone="13900000000", gender=1)

    def test_user_info_fields(self):
        # 测试模型的字段是否符合预期
        alice = UserInfo.objects.get(user="Alice")
        bob = UserInfo.objects.get(user="Bob")
        self.assertEqual(alice.user, "Alice")
        self.assertEqual(alice.password, "123456")
        self.assertEqual(alice.email, "alice@example.com")
        self.assertEqual(alice.mobile_phone, "13800000000")
        self.assertEqual(alice.gender, 0)
        self.assertEqual(bob.user, "Bob")
        self.assertEqual(bob.password, "654321")
        self.assertEqual(bob.email, "bob@example.com")
        self.assertEqual(bob.mobile_phone, "13900000000")
        self.assertEqual(bob.gender, 1)

    def test_user_info_str(self):
        # 测试模型的 __str__ 方法是否正确返回 user 属性
        alice = UserInfo.objects.get(user="Alice")
        bob = UserInfo.objects.get(user="Bob")
        self.assertEqual(str(alice), "Alice")
        self.assertEqual(str(bob), "Bob")

    def test_user_info_get_gender_display(self):
        # 测试模型的 get_gender_display 方法是否正确返回 gender_choices 中对应的值
        alice = UserInfo.objects.get(user="Alice")
        bob = UserInfo.objects.get(user="Bob")
        self.assertEqual(alice.get_gender_display(), "女")
        self.assertEqual(bob.get_gender_display(), "男")
        print(f"self id in test_book_title: {id(self)}")

    def test_user_info_verbose_name(self):
        # 测试模型的 verbose_name 是否符合预期
        user_info = UserInfo()
        self.assertEqual(user_info._meta.verbose_name, "用户信息")

    def test_user_info_verbose_name_plural(self):
        # 测试模型的 verbose_name_plural 是否符合预期
        user_info = UserInfo()
        self.assertEqual(user_info._meta.verbose_name_plural, "用户信息")

    def test_user_info_field_verbose_name(self):
        # 测试模型的字段的 verbose_name 是否符合预期
        user_info = UserInfo()
        self.assertEqual(user_info._meta.get_field("user").verbose_name, "用户名")
        self.assertEqual(user_info._meta.get_field("password").verbose_name, "密码")
        self.assertEqual(user_info._meta.get_field("email").verbose_name, "邮箱")
        self.assertEqual(user_info._meta.get_field("mobile_phone").verbose_name, "手机号")
        self.assertEqual(user_info._meta.get_field("gender").verbose_name, "性别")

    def test_user_info_field_max_length(self):
        # 测试模型的字段的 max_length 是否符合预期
        user_info = UserInfo()
        self.assertEqual(user_info._meta.get_field("user").max_length, 32)
        self.assertEqual(user_info._meta.get_field("password").max_length, 64)
        self.assertEqual(user_info._meta.get_field("email").max_length, 32)
        self.assertEqual(user_info._meta.get_field("mobile_phone").max_length, 32)

    def test_user_info_field_choices(self):
        # 测试模型的字段的 choices 是否符合预期
        user_info = UserInfo()
        gender_choices = [
            (1, "男"),
            (0, "女"),
         ]
        self.assertListEqual(list(user_info._meta.get_field("gender").choices), gender_choices)
