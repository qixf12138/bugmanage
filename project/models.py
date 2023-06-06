from django.db import models
from user.models import UserInfo


# 项目类
class ProjectInfo(models.Model):
    COLOR_CHOICES = (
        (1, "#56b8eb"),
        (2, "#f28033"),
        (3, "#ebc656"),
        (4, "#a2d148"),
        (5, "#20bfa4"),
        (6, "#7461c2"),
        (7, "#20bfa3"),
    )
    name = models.CharField(verbose_name="项目名称",  max_length=32)
    color = models.SmallIntegerField(verbose_name="颜色", choices=COLOR_CHOICES, default=1)
    describe = models.TextField(verbose_name="项目简介", max_length=256, null=True, blank=True)
    star_mark = models.BooleanField(verbose_name="星标", default=False)

    # bucket = models.CharField(verbose_name="腾讯云对象储存桶", max_length=128)
    # regin = models.CharField(verbose_name="腾讯云对象储存桶区域", max_length=32)

    creator = models.ForeignKey(verbose_name="创建人", to="user.UserInfo",
                                on_delete=models.CASCADE, to_field="id")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class ProjectUser(models.Model):
    """
    用户与项目表的对应关系（参与项目的人）
    """
    user = models.ForeignKey(verbose_name="用户", to="user.UserInfo",
                             to_field="id", on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name="项目", to="ProjectInfo",
                                to_field="id", on_delete=models.CASCADE)
    star_mark = models.BooleanField(verbose_name="星标", default=False)
    create_time = models.DateTimeField(verbose_name="加入时间", auto_now_add=True)

    class Meta:
        unique_together = ["user", "project"]


class PricePolicy(models.Model):
    """
    价格策略
    """
    category_choices = (
        (1, "免费版"),
        (2, "VIP"),
        (3, "SVIP"),
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=category_choices, default=1)
    price = models.PositiveIntegerField(verbose_name="价格")
    create_project = models.PositiveIntegerField(verbose_name="创建项目上限")
    project_user = models.PositiveIntegerField(verbose_name="项目成员上限")
    project_capacity = models.PositiveIntegerField(verbose_name="项目空间")
    file_capacity = models.PositiveIntegerField(verbose_name="单文件上限")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
