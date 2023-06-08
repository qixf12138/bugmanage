from django.urls import path
from system.views import ProjectList, ProjectManage, ProjectAdd, ProjectAlter, ProjectStarMark

# /system/
urlpatterns = [
    path("", ProjectManage.as_view(), name="index"),
    path("list/", ProjectList.as_view(), name="list"),
    path("add/", ProjectAdd.as_view(), name="add"),
    path("alter/", ProjectAlter.as_view(), name="alter"),
    path("star/", ProjectStarMark.as_view(), name="star"),

]