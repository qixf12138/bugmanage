from bugmanage import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LoginVerification(MiddlewareMixin):

    exclued_path = ["/user/login/", "/user/smslogin/", "/user/register/",
                    "/user/sendsms/", "/user/vcode/", "/static/"]

    def process_request(self, request):
        if request.path in self.exclued_path:
            return
        else:
            user = request.session.get("user")
            if user:
                return
            else:
                return redirect(settings.LOGOUT_REDIRECT_URL)

    def process_response(self, request, response):
        return response
