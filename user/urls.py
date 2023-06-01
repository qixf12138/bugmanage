from django.urls import path
from user import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sendsms/", views.send_short_msg, name="sendsms"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("smslogin/", views.user_login_sms, name="smslogin"),
    path("info/", views.user_info, name="userinfo"),

]
