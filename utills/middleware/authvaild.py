import uuid

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

import re
from bugmanage import settings
from project.models import ProjectInfo
from user.models import UserInfo
from system.models import Transaction
from utills.projectutills.tools import get_now_data_str


class UserInfomation():
    """
    封装用户信息
    """
    def __init__(self, user, policy):
        self.user = user
        self.policy = policy


class LoginVerification(MiddlewareMixin):

    exclued_path = ["/user/login/", "/user/smslogin/", "/user/register/",
                    "/user/sendsms/", "/user/vcode/", "/static/"]

    def process_request(self, request):
        # 白名单不需要登录即可访问
        if request.path in self.exclued_path:
            return

        # 从session获取用户名
        user = request.session.get("user")
        # 从session获取到用户后查询用户是否存在
        user = UserInfo.objects.filter(user=user).first()

        if user:
            # 查询是否有订单存在,获取最新订单状态，存放在request中
            transaction = Transaction.objects.filter(user=user).order_by("-id").first()
            # 如果查询不到, 则创建一条免费的订单
            if not transaction:
                transaction = Transaction.objects.create(order=uuid.uuid4(), status=2, price_policy_id=1,
                                                         user=user, count_year=0, pay=0,
                                                         start_time=get_now_data_str(), end_time=None)

            request.userinfo = UserInfomation(user=user, policy=transaction.price_policy)
            # request.transaction = transaction
            # request.user = user
            return

        # 用户没有查询到,清除session相关信息
        else:
            request.session.clear()

        return redirect(settings.LOGOUT_REDIRECT_URL)

    def process_response(self, request, response):
        return response


class ProjectManageNavbar(MiddlewareMixin):
    pattern = r"/project/\d+/.+"

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not re.match(self.pattern, request.path):
            return
        now_tag = request.path.split("/")[3]
        proejct_id = view_kwargs.get("project_id")
        user = request.userinfo.user
        project = ProjectInfo.objects.filter(id=proejct_id, creator=user).first()
        if project:
            request.userinfo.project = project
            request.now_tag = now_tag
        else:
           return redirect(settings.LOGOUT_REDIRECT_URL)

