from django.urls import path
from user import views

urlpatterns = [
    path("send_sms/", views.send_short_msg, name="send_sms"),
]