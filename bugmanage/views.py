from django.views import View
from django.http import JsonResponse
from django.shortcuts import render


class BaseJsonView(View):
    # 返回Json格式
    @staticmethod
    def success_response():
        content = {"status": 200}
        return JsonResponse(content)

    @staticmethod
    def error_response(error_msg):
        content = {"status": 400, "error_msg": error_msg}
        return JsonResponse(content)

    @staticmethod
    def success_response_data(content):
        if not isinstance(content, dict):
            raise ValueError("参数content必须为字典类型")
        content["status"] = 200
        return JsonResponse(content)

    @staticmethod
    def error_response_data(content):
        if not isinstance(content, dict):
            raise ValueError("参数content必须为字典类型")
        content["status"] = 400
        return JsonResponse(content)

# class BaseHtmlView(View):
#     # 返回html格式
#     @staticmethod
#     def success_response(template, content):
#         return render()
