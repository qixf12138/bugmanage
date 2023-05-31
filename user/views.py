import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from bugmanage import settings
from django_redis import get_redis_connection

from utills.tencent.sms import send_sms
from utills.projectutills.tools import generate_code, valid_code
from utills.datavalid.datavalid import mobilephone_number_vaild
from user.forms import RegisterModelForm


def send_short_msg(request):
    """
    发送短信验证码
    :param request:
    :return:验证手机号码格式，如果错误，将返回错误信息。手机号码格式验证通过，返回success字符串。
    """
    # 获取短信模板ID
    req = request.GET.get("req")
    template_id = settings.TENCENT_SMS_TEMPLATES.get(req)
    context_dict = {}
    if not template_id:
        context_dict["error_msg"] = "请求错误,sms模板不存在"
        return JsonResponse(context_dict)
    # 获取输入的用户手机号
    mobile_phone = request.GET.get("mobile_phone")
    print(mobile_phone)
    if mobile_phone:
        # 进行手机号格式验证
        ret = mobilephone_number_vaild(mobile_phone)
        if ret:
            # 生成随机验证码,放到短信参数列表中
            code = generate_code(mobile_phone)
            mobile_phone_list = ["+86" + mobile_phone]
            sms_param_list = [code]
        else:
            context_dict["error_msg"] = "手机号格式不正确"
            return JsonResponse(context_dict)
    else:
        context_dict["error_msg"] = "手机号未填写"
        return JsonResponse(context_dict)
    # 发送手机验证码 (2023.5.31发送成功，注释省钱~~)
    #send_sms(sms_param_list, mobile_phone_list, template_id)
    context_dict["status"] = "200"
    context_dict["code"] = code
    return JsonResponse(context_dict)


def user_register(request):
    """
    用户注册
    """
    if request.method == "GET":
        form = RegisterModelForm()
    elif request.method == "POST":
        form = RegisterModelForm(data=request.POST)
        context_dict = {}
        # 验证手机验证码是否正确
        if form.is_valid():
            # 获取用户输入的验证码
            user_code = form.cleaned_data["code"]
            mobile_phone = form.cleaned_data["mobile_phone"]
            if not valid_code(mobile_phone, user_code):
                form.add_error("code", "验证码错误!")
                context_dict["error_msg"] = form.errors
            else:
                context_dict["status"] = 200
                form.save()
            return JsonResponse(context_dict)
        else:
            context_dict["error_msg"] = form.errors
            return JsonResponse(context_dict)
    else:
        return JsonResponse("请求方法错误")
    return render(request, "user/register.html", {"form": form})


def index(request):
    # redis 连接测试
    conn = get_redis_connection("default")
    conn.set("nickname", "77777", ex=10)
    value = conn.get("nickname")
    print(value)
    return HttpResponse(value)

