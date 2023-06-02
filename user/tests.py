from django.test import TestCase
from user.models import UserInfo
from django.test import TestCase, Client
# 导入你的视图函数


class UserInfoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 创建一些测试数据，只在类级别执行一次
        UserInfo.objects.create(user="Alice", password="123456", email="alice@example.com", mobile_phone="13800000000")
        UserInfo.objects.create(user="Bob", password="654321", email="bob@example.com", mobile_phone="13900000000")

    def test_user_info_fields(self):
        # 测试模型的字段是否符合预期
        alice = UserInfo.objects.get(user="Alice")
        bob = UserInfo.objects.get(user="Bob")
        self.assertEqual(alice.user, "Alice")
        self.assertEqual(alice.password, "123456")
        self.assertEqual(alice.email, "alice@example.com")
        self.assertEqual(alice.mobile_phone, "13800000000")
        self.assertEqual(bob.user, "Bob")
        self.assertEqual(bob.password, "654321")
        self.assertEqual(bob.email, "bob@example.com")
        self.assertEqual(bob.mobile_phone, "13900000000")

    def test_user_info_str(self):
        # 测试模型的 __str__ 方法是否正确返回 user 属性
        alice = UserInfo.objects.get(user="Alice")
        bob = UserInfo.objects.get(user="Bob")
        self.assertEqual(str(alice), "Alice")
        self.assertEqual(str(bob), "Bob")

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

    def test_user_info_field_max_length(self):
        # 测试模型的字段的 max_length 是否符合预期
        user_info = UserInfo()
        self.assertEqual(user_info._meta.get_field("user").max_length, 32)
        self.assertEqual(user_info._meta.get_field("password").max_length, 64)
        self.assertEqual(user_info._meta.get_field("email").max_length, 32)
        self.assertEqual(user_info._meta.get_field("mobile_phone").max_length, 32)


# 创建一个测试类，继承自TestCase
class ViewsTest(TestCase):
    # 在每个测试方法之前运行，设置一些初始数据
    def setUp(self):
        # 创建一个测试客户端
        self.client = Client()
        # 创建一个测试用户
        self.user = UserInfo.objects.create(user="test", password="password", mobile_phone="12345678901")

    # 测试send_short_msg视图函数
    def test_send_short_msg(self):
        # 测试没有req参数的情况，应该返回错误信息
        response = self.client.get("/user/sendsms/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"error_msg": "请求错误,sms模板不存在"})

        # 测试有req参数但是没有mobile_phone参数的情况，应该返回错误信息
        response = self.client.get("/user/sendsms/?req=register")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"error_msg": "手机号未填写"})

        # 测试有req参数和mobile_phone参数，但是手机号格式不正确的情况，应该返回错误信息
        response = self.client.get("/user/sendsms/?req=register&mobile_phone=123")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"error_msg": "手机号格式不正确"})

        # 测试有req参数和mobile_phone参数，且手机号格式正确的情况，应该返回成功信息和验证码
        response = self.client.get("/user/sendsms/?req=register&mobile_phone=12345678901")
        self.assertEqual(response.status_code, 200)

    # 测试user_register视图函数
    def test_user_register(self):
        # 测试GET请求，应该返回注册表单
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

        # 测试POST请求，但是没有输入验证码，应该返回错误信息
        response = self.client.post("/user/register/", {
            "user": "test2",
            "password": "password",
            "confirm_password": "password",
            "mobile_phone": "13100000000",
            "code": "",
            "email": "1234@1234.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"error_msg": {"code": ["这个字段是必填项。"]}})

        # 测试POST请求，但是输入了错误的验证码，应该返回错误信息
        response = self.client.post("/user/register/", {
            "user": "test2",
            "password": "password",
            "confirm_password": "password",
            "mobile_phone": "13500000001",
            "code": "123456",
            "email": "1234@1234.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"error_msg": {"code": ["验证码错误!"]}})

        # 测试POST请求，且输入了正确的验证码，应该返回成功信息和重定向地址
        # 先用send_short_msg视图函数获取正确的验证码
        code_response = self.client.get("/user/sendsms/?req=register&mobile_phone=13676777777")
        code = code_response.json()["code"]

        response = self.client.post("/user/register/", {
            "user": "test2",
            "password": "password",
            "confirm_password": "password",
            "mobile_phone": "13676777777",
            "code": code,
            "email": "99988@88.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("redirect_url", response.json())

    # 测试verif_code视图函数
    def test_verif_code(self):
        # 测试GET请求，应该返回一个图片验证码，并且在session中保存字符串验证码
        response = self.client.get("/user/vcode/")
        self.assertEqual(response.status_code, 200)
