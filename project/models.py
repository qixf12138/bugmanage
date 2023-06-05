from django.db import models
from user.models import UserInfo


# 项目类
class ProjectInfo(models.Model):
    COLOR_CHOICES = (
        (1, "#56b8eb"),
        (2, "#f28033"),
        (3, "#ebc656"),
        (4, "#a2d148"),
        (5, "#20BFA4"),
        (6, "#7461c2"),
        (7, "#20bfa3"),
    )
    name = models.CharField(verbose_name="项目名称",  max_length=32)
    color = models.SmallIntegerField(verbose_name="颜色", choices=COLOR_CHOICES, default=1)
    describe = models.TextField(verbose_name="项目简介", max_length=256)
    use_space = models.IntegerField(verbose_name="项目使用空间", default=False)
    user = models.ForeignKey(verbose_name="创建人", to="user.UserInfo", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间")


# 用户与项目表的对应关系（参与项目的人）
class UserJoinProjectInfo(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="user.UserInfo",
                             to_field="id", on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name="项目", to="project.ProjectInfo",
                                to_field="id", on_delete=models.CASCADE)
    star_mark = models.BooleanField(verbose_name="星标", default=False)

    class Meta:
        unique_together = ["user", "project"]
