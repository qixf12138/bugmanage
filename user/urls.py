from django.urls import path
from user import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_sms/", views.send_short_msg, name="send_sms"),
    path("register/", views.user_register, name="register"),
]
