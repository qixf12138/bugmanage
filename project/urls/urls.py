from django.urls import path, include
from project.views.views import *

app_name = "project"

urlpatterns = [
    path("", ProjectManage.as_view(), name="index"),
    path("list/", ProjectList.as_view(), name="list"),
    path("add/", ProjectAdd.as_view(), name="add"),
    path("alter/", ProjectAlter.as_view(), name="alter"),
    path("star/", ProjectStarMark.as_view(), name="star"),
    path("<int:project_id>/", include("project.urls.project_manage_urls", namespace="operate")),
]