from django.urls import path
from project.views.manage_views import *

"""
进入项目页面后相关操作的url
"""

app_name = "operate"

urlpatterns = [
        path("overview/", ProjectOverView.as_view(), name="overview"),
        path("issue/", ProjectIssue.as_view(), name="issue"),
        path("analyze/", ProjectAnalyze.as_view(), name="analyze"),
        path("file/", ProjectFile.as_view(), name="file"),
        path("file/upload", ProjectUploadFile.as_view(), name="file_upload"),
        path("wiki/", ProjectWiki.as_view(), name="wiki"),
        # path("wiki/<int:wiki_id>/", ProjectWikiDesc.as_view(), name="wiki_desc"),
        path("wiki/alter/", ProjectWikiAlter.as_view(), name="wiki_alter"),
        path("wiki/delete/", project_wiki_delete, name="wiki_delete"),
        path("wiki/add/", ProjectWikiAdd.as_view(), name="wiki_add"),
        path("wiki/upload/", project_wili_upload, name="wiki_upload"),
        path("wiki/title/", ProjectWikiTitle.as_view(), name="wiki_title"),
        path("settings/", ProjectSettings.as_view(), name="settings"),
]
