from django.urls import path
from user import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sendsms/", views.SendShortMSG.as_view(), name="sendsms"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("smslogin/", views.UserSMSLogin.as_view(), name="smslogin"),
    path("info/", views.user_info, name="userinfo"),
    path("vcode/", views.verif_code, name="verifcode")

]
