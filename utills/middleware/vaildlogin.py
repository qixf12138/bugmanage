import uuid

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

from bugmanage import settings
from user.models import UserInfo
from system.models import Transaction
from utills.projectutills.tools import get_now_data_str


class LoginVerification(MiddlewareMixin):

    exclued_path = ["/user/login/", "/user/smslogin/", "/user/register/",
                    "/user/sendsms/", "/user/vcode/", "/static/"]

    def process_request(self, request):
        # 白名单不需要登录即可访问
        if request.path in self.exclued_path:
            return

        # 从session获取用户名
        user = request.session.get("user")
        if user:
            # 从session获取到用户后查询用户是否存在
            user = UserInfo.objects.filter(user=user)
            if user.exists():
                # 查询是否有订单存在,获取最新订单状态，存放在request中
                transaction = Transaction.objects.filter(user=user.first()).order_by("-id").first()
                # 如果查询不到, 则创建一条免费的订单
                if not transaction:
                    transaction = Transaction.objects.create(order=uuid.uuid4(), status=2, price_policy_id=1,
                                                             user=user.first(), count_year=0, pay=0,
                                                             start_time=get_now_data_str(), end_time=None)
                request.transaction = transaction
                return

            # 用户没有查询到,清除session相关信息
            else:
                request.session.clear()
        return redirect(settings.LOGOUT_REDIRECT_URL)

    def process_response(self, request, response):
        return response
