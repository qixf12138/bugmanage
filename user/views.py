import random
from io import BytesIO

import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bugmanage import settings
from django_redis import get_redis_connection

from bugmanage.views import BaseJsonView
from user.models import UserInfo
from utills.tencent.sms import send_sms
from utills.projectutills.tools import generate_code, valid_code, ip_is_limit
from utills.datavalid.datavalid import mobilephone_number_vaild
from utills.projectutills.randomobj import create_random_str, create_vcode_img
from utills.projectutills.encrypt import md5
from user.forms import RegisterModelForm, SMSLoginModelForm, LoginModelForm


# def send_short_msg(request):
#     """
#     发送短信验证码
#     :param request:
#     :return:验证手机号码格式，如果错误，将返回错误信息。手机号码格式验证通过，返回success字符串。
#     """
#     # 获取短信模板ID
#     req = request.GET.get("req")
#     template_id = settings.TENCENT_SMS_TEMPLATES.get(req)
#     content = {}
#     if not template_id:
#         content["error_msg"] = "请求错误,sms模板不存在"
#         return JsonResponse(content)
#     # 获取输入的用户手机号
#     mobile_phone = request.GET.get("mobile_phone")
#     if mobile_phone:
#         # 进行手机号格式验证
#         ret = mobilephone_number_vaild(mobile_phone)
#         if ret:
#             # 查看请求是否被限制
#             if ip_is_limit(request):
#                 content["error_msg"] = "发送速度太快，请休息1分钟"
#                 return JsonResponse(content)
#             # 生成随机验证码,放到短信参数列表中
#             code = generate_code(mobile_phone)
#             mobile_phone_list = ["+86" + mobile_phone]
#             sms_param_list = [code]
#         else:
#             content["error_msg"] = "手机号格式不正确"
#             return JsonResponse(content)
#     else:
#         content["error_msg"] = "手机号未填写"
#         return JsonResponse(content)
#     # 发送手机验证码 (2023.5.31发送成功，注释省钱~~)
#     #send_sms(sms_param_list, mobile_phone_list, template_id)
#     content["status"] = "200"
#     content["code"] = code
#     return JsonResponse(content)
class SendShortMSG(BaseJsonView):
    """
    获取短信验证码
    get():return:验证手机号码格式，如果错误，将返回错误信息。手机号码格式验证通过，返回success字符串。
    """
    def get(self, request):
        # 获取短信模板ID
        req = request.GET.get("req")
        template_id = settings.TENCENT_SMS_TEMPLATES.get(req)
        if not template_id:
            return self.error_response("请求错误,sms模板不存在")

        # 获取输入的用户手机号,验证手机号格式是否正确
        mobile_phone = request.GET.get("mobile_phone")
        ret = mobilephone_number_vaild(mobile_phone)

        if ret:
            # 查看请求是否被限制
            if ip_is_limit(request):
                return self.error_response("发送速度太快，请休息1分钟")

            # 生成随机验证码,放到短信参数列表中
            code = generate_code(mobile_phone)
            mobile_phone_list = ["+86" + mobile_phone]
            sms_param_list = [code]
        else:
            return self.error_response("手机号格式不正确")

        # 发送手机验证码 (2023.5.31发送成功，注释省钱~~)
        # send_sms(sms_param_list, mobile_phone_list, template_id)
        # 返回前端，证实使用的时候可以删除
        content = {"code": code }
        return self.success_response_data(content)


# def user_register(request):
#     """
#     用户注册
#     """
#     if request.method == "GET":
#         form = RegisterModelForm()
#     elif request.method == "POST":
#         form = RegisterModelForm(data=request.POST)
#         content = {}
#         # 验证手机验证码是否正确
#         if form.is_valid():
#             # 获取用户输入的验证码
#             user_code = form.cleaned_data["code"]
#             mobile_phone = form.cleaned_data["mobile_phone"]
#             print("注册表单验证通过")
#             print(mobile_phone, user_code)
#             print(valid_code(mobile_phone, user_code))
#             if not valid_code(mobile_phone, user_code):
#                 form.add_error("code", "验证码错误!")
#                 content["error_msg"] = form.errors
#             else:
#                 form.save()
#                 request.session["user"] = form.cleaned_data.get("user")
#                 content["status"] = 304
#                 content["redirect_url"] = settings.LOGIN_REDIRECT_URL
#                 return JsonResponse(content)
#         else:
#             content["error_msg"] = form.errors
#             return JsonResponse(content)
#     else:
#         return JsonResponse("请求方法错误")
#     return render(request, "user/register.html", {"form": form})
class UserRegister(BaseJsonView):
    """
    用户注册
    """
    template_name = "user/register.html"

    def get(self, request):
        if request.method == "GET":
            form = RegisterModelForm()
            return render(request, UserRegister.template_name, {"form": form})

    def post(self, request):
        form = RegisterModelForm(data=request.POST)

        # 验证手机验证码是否正确
        if form.is_valid():
            # 获取用户输入的验证码,获取用户手机号
            user_code = form.cleaned_data["code"]
            mobile_phone = form.cleaned_data["mobile_phone"]

            if not valid_code(mobile_phone, user_code):
                form.add_error("code", "验证码错误!")
                print("验证码错误")
            else:
                form.save()
                request.session["user"] = form.cleaned_data.get("user")
                content = {"redirect_url" : settings.LOGIN_REDIRECT_URL}
                return self.success_response_data(content)
        content = {"error_msg": form.errors}
        return self.error_response_data(content)


# def user_login(request):
#     if request.method == "GET":
#         sms_form = SMSLoginModelForm()
#         user_form = LoginModelForm()
#         content = {"sms_form": sms_form,
#                    "user_form": user_form}
#
#     elif request.method == "POST":
#         content = {}
#         user_form = LoginModelForm(data=request.POST)
#
#         try:
#             # 如果用户没输入的验证码，或者没有获取验证码，捕获异常，返回验证码错误
#             code = request.session.get("img_code").upper()
#             user_input_code = request.POST.get("img_code").upper()
#         except Exception as e :
#             # 清除表单自带的数据,实现先显示验证码，再验证账号。
#             user_form.errors.clear()
#             user_form.add_error("img_code", "验证码错误！")
#             content["error_msg"] = user_form.errors
#             return JsonResponse(content)
#         # 验证码验证通过
#         if code == user_input_code:
#             # 表单验证
#             if user_form.is_valid():
#                 user_name = user_form.cleaned_data.get("user")
#                 user = UserInfo.objects.filter(user=user_name).first()
#                 # 保存登录状态
#                 request.session["user"] = user.user
#                 request.session["id"] = user.id
#                 content["status"] = 304
#                 content["redirect_url"] = settings.LOGIN_REDIRECT_URL
#                 # 重置验证码，让之前的验证码失效
#                 request.session["img_code"] = create_random_str(6)
#                 return JsonResponse(content)
#             else:
#                 content["status"] = 403
#         else:
#             # 验证码验证不通过,清除额外的验证信息，只返回验证码错误提示
#             user_form.errors.clear()
#             user_form.add_error("img_code", "验证码错误！")
#         content["error_msg"] = user_form.errors
#         return JsonResponse(content)
#     else:
#         return HttpResponse("请求方式错误")
#     return render(request, "user/login.html", content)
class UserLogin(BaseJsonView):
    """
    使用用户名密码登录

    """
    templates_name = "user/login.html"

    # 登录页面(账号登陆和手机号登录)
    def get(self, request):
        sms_form = SMSLoginModelForm()
        user_form = LoginModelForm()
        content = {"sms_form": sms_form,
                   "user_form": user_form}
        return render(request, UserLogin.templates_name, content)

    def post(self, request):
        user_form = LoginModelForm(data=request.POST)
        try:
            # 如果用户没输入的验证码，或者没有获取验证码，捕获异常，返回验证码错误
            code = request.session.get("img_code").upper()
            user_input_code = request.POST.get("img_code").upper()
            content = {}
        except Exception as e:
            # 清除表单自带的数据,实现先显示验证码，再验证账号。
            user_form.errors.clear()
            user_form.add_error("img_code", "验证码错误！")
            content["error_msg"] = user_form.errors
            return self.error_response_data(content)

        if code == user_input_code:
            # 验证码验证通过，进行表单验证
            if user_form.is_valid():
                user_name = user_form.cleaned_data.get("user")
                user = UserInfo.objects.filter(user=user_name).first()

                if user:
                    # 保存登录状态
                    request.session["user"] = user.user
                    request.session["id"] = user.id
                    content["redirect_url"] = settings.LOGIN_REDIRECT_URL

                    # 重置验证码，让之前的验证码失效
                    request.session["img_code"] = create_random_str(6)
                    return self.success_response_data(content)
            else:
                content["error_msg"] = user_form.errors
                return self.error_response_data(content)
        else:
            # 验证码验证不通过,清除额外的验证信息，只返回验证码错误提示
            user_form.errors.clear()
            user_form.add_error("img_code", "验证码错误！")
            content["error_msg"] = user_form.errors
        return self.error_response_data(content)


# Ajax SMS登录请求
# def user_login_sms(request):
#     if request.method == "POST":
#         content = {}
#         form = SMSLoginModelForm(data=request.POST)
#         if form.is_valid():
#             mobile_phone = form.cleaned_data['mobile_phone']
#             user = UserInfo.objects.filter(mobile_phone=mobile_phone).first()
#             content["status"] = 304
#             if user:
#                 # 登陆成功，跳转用户信息页面
#                 print("登陆成功")
#                 request.session["user"] = user.user
#                 request.session["id"] = user.id
#                 content["redirect_url"] = settings.LOGIN_REDIRECT_URL
#             else:
#                 # 没有注册，随机生成用户名
#                 user_name = "user_" + create_random_str()
#                 mobile_phone = form.cleaned_data.get("mobile_phone")
#                 password = md5("123456")
#                 user = UserInfo.objects.create(user=user_name, password=password, mobile_phone=mobile_phone, email="")
#                 request.session["user"] = user.user
#                 request.session["id"] = user.id
#                 content["redirect_url"] = settings.LOGIN_REDIRECT_URL
#                 return JsonResponse(content)
#         else:
#             print("验证失败")
#             content = {"error_msg": form.errors}
#         return JsonResponse(content)
#     else:
#         print("请求失败")
#         return JsonResponse({"error_msg": "请求错误"})
class UserSMSLogin(BaseJsonView):
    """
    AJAX方式请求
    短信验证码方式登录
    """

    def post(self, request):
        form = SMSLoginModelForm(data=request.POST)
        if form.is_valid():
            mobile_phone = form.cleaned_data['mobile_phone']
            user = UserInfo.objects.filter(mobile_phone=mobile_phone).first()

            if user:
                # 登陆成功，已经注册,跳转用户信息页面
                print("登陆成功")
                request.session["user"] = user.user
                request.session["id"] = user.id

            else:
                # 没有注册，随机生成用户名,初始密码：123456,将用户名和id加入的session中
                user_name = "user_" + create_random_str()
                mobile_phone = form.cleaned_data.get("mobile_phone")
                password = md5(settings.INIT_USER_PASSWORD)
                user = UserInfo.objects.create(user=user_name, password=password, mobile_phone=mobile_phone, email="")
                request.session["user"] = user.user
                request.session["id"] = user.id

            # 登录成功,返回跳转路径
            content = {"redirect_url": settings.LOGIN_REDIRECT_URL}
            return self.success_response_data(content)

        # 验证不通过
        content = {"error_msg": form.errors}
        return self.error_response_data(content)


def verif_code(request):
    # 生成验证码，字符串验证码加入session,返回图片验证码
    img, code = create_vcode_img()
    request.session["img_code"] = code
    #request.session.set_expiry(60*24)
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())


def user_info(request):
    content = {}
    username = request.session.get("user")
    if username:
        user = UserInfo.objects.filter(user=username).first()
        content["user"] = user
    return render(request, "user/userinfo.html", content)


def user_logout(request):
    request.session.clear()
    return redirect(settings.LOGOUT_REDIRECT_URL)


def index(request):
    return HttpResponse(0)


