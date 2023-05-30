import random

from django.shortcuts import render, HttpResponse
from bugmanage import settings

from utills.tencent.sms import send_sms
from utills.datavalid.datavalid import mobilephone_number_vaild


def send_short_msg(request):
    """
    发送短信验证码
    :param request:
    :return:
    """
    # 获取短信模板ID
    req = request.GET.get("req")
    template_id = settings.TENCENT_SMS_TEMPLATES.get(req)
    if not template_id:
        return HttpResponse("请求错误,sms模板不存在")

    # 生成随机验证码,放到短信参数列表中
    param_list = [str(random.randrange(100000, 999999))]

    # 获取用户手机号，如果格式正确，放到收信人列表中
    phone_number = request.GET.get("phone_number")
    if phone_number:
        ret = mobilephone_number_vaild(phone_number)
        if ret:
            phone_number_list = ["+86" + phone_number]
        else:
            return HttpResponse("手机号格式不正确")
    else:
        return HttpResponse("请求错误,手机号码未填写")
    # 发送手机验证码 (2023.5.30发送成功，注释省钱~~)
    # send_sms(param_list, phone_number_list, template_id)
    return HttpResponse("success")

