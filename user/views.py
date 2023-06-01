import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from bugmanage import settings
from django_redis import get_redis_connection

from user.models import UserInfo
from utills.tencent.sms import send_sms
from utills.projectutills.tools import generate_code, valid_code, ip_is_limit
from utills.datavalid.datavalid import mobilephone_number_vaild
from utills.projectutills.randomobj import create_random_str
from utills.projectutills.encrypt import md5
from user.forms import RegisterModelForm, SMSLoginModelForm


def send_short_msg(request):
    """
    发送短信验证码
    :param request:
    :return:验证手机号码格式，如果错误，将返回错误信息。手机号码格式验证通过，返回success字符串。
    """
    # 获取短信模板ID
    req = request.GET.get("req")
    template_id = settings.TENCENT_SMS_TEMPLATES.get(req)
    content = {}
    if not template_id:
        content["error_msg"] = "请求错误,sms模板不存在"
        return JsonResponse(content)
    # 获取输入的用户手机号
    mobile_phone = request.GET.get("mobile_phone")
    if mobile_phone:
        # 进行手机号格式验证
        ret = mobilephone_number_vaild(mobile_phone)
        if ret:
            # 查看请求是否被限制
            if ip_is_limit(request):
                content["error_msg"] = "发送速度太快，请休息1分钟"
                return JsonResponse(content)
            # 生成随机验证码,放到短信参数列表中
            code = generate_code(mobile_phone)
            mobile_phone_list = ["+86" + mobile_phone]
            sms_param_list = [code]
        else:
            content["error_msg"] = "手机号格式不正确"
            return JsonResponse(content)
    else:
        content["error_msg"] = "手机号未填写"
        return JsonResponse(content)
    # 发送手机验证码 (2023.5.31发送成功，注释省钱~~)
    #send_sms(sms_param_list, mobile_phone_list, template_id)
    content["status"] = "200"
    content["code"] = code
    return JsonResponse(content)


def user_register(request):
    """
    用户注册
    """
    if request.method == "GET":
        form = RegisterModelForm()
    elif request.method == "POST":
        form = RegisterModelForm(data=request.POST)
        content = {}
        # 验证手机验证码是否正确
        if form.is_valid():
            # 获取用户输入的验证码
            user_code = form.cleaned_data["code"]
            mobile_phone = form.cleaned_data["mobile_phone"]
            if not valid_code(mobile_phone, user_code):
                form.add_error("code", "验证码错误!")
                content["error_msg"] = form.errors
            else:
                form.save()
                request.session["info"] = form.cleaned_data.get("user")
                content["status"] = 304
                content["redirect_url"] = settings.LOGIN_REDIRECT_URL
            return JsonResponse(content)
        else:
            content["error_msg"] = form.errors
            return JsonResponse(content)
    else:
        return JsonResponse("请求方法错误")
    return render(request, "user/register.html", {"form": form})


# 登录页面和密码登录请求
def user_login(request):
    if request.method == "GET":
        form = SMSLoginModelForm()
        content = {"form": form}
    return render(request, "user/login.html", content)


# Ajax SMS登录请求
def user_login_sms(request):
    if request.method == "POST":
        content = {}
        form = SMSLoginModelForm(data=request.POST)
        if form.is_valid():
            mobile_phone = form.cleaned_data['mobile_phone']
            user = UserInfo.objects.filter(mobile_phone=mobile_phone).first()
            content["status"] = 304
            if user:
                # 登陆成功，跳转用户信息页面
                print("登陆成功")
                request.session["info"] = user.user
                content["redirect_url"] = settings.LOGIN_REDIRECT_URL
            else:
                # 没有注册，随机生成用户名
                user_name = "user_" + create_random_str()
                mobile_phone = form.cleaned_data.get("mobile_phone")
                password = md5("123456")
                user = UserInfo.objects.create(user=user_name, password=password, mobile_phone=mobile_phone)
                request.session["info"] = user.user
                content["redirect_url"] = settings.LOGIN_REDIRECT_URL
        else:
            print("验证失败")
            content = {"error_msg": form.errors}
        return JsonResponse(content)
    else:
        print("请求失败")
        return JsonResponse({"error_msg": "请求错误"})


def user_info(request):
    content = {}
    username = request.session.get("info")
    if username:
        user = UserInfo.objects.filter(user=username).first()
        content["user"] = user
    return render(request, "user/userinfo.html", content)


def user_logout(request):
    request.session.clear()
    return redirect(settings.LOGOUT_REDIRECT_URL)


def index(request):
    return HttpResponse(0)


