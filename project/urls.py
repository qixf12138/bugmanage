from django.urls import path
from project import views

urlpatterns = [
    path("list/", views.project_list, name="mylist"),
    path("alter/", views.project_alter, name="alter"),
    path("star/", views.project_star_mark, name="star"),

]