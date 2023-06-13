from django.test import TestCase
from project.models import ProjectUser


class ProjectToUserInfoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 创建一些测试数据，只在类级别执行一次
        ProjectUser.objects.create(user_id=1, project_id=1, star_mark=True)
        ProjectUser.objects.create(user_id="2", project_id="1", star_mark=True)


    def test_add_user_to_project(self):
        ProjectUser.objects.create(user_id=3, project_id=2, star_mark=True)
        ProjectUser.objects.create(user_id=4, project_id=2, star_mark=True)
