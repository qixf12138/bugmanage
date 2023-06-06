from django.db import models


class Transaction(models.Model):
    status_choices = (
        (1, "未支付"),
        (2, "已支付")
    )
    order = models.CharField(verbose_name="订单号", max_length=64, unique=True)
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices)
    user = models.ForeignKey(verbose_name="用户", to="user.UserInfo", on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name="购买等级", to="project.PricePolicy",
                                     on_delete=models.CASCADE)
    count_year = models.SmallIntegerField(verbose_name="购买数量(年)", help_text="0表示无限期")
    pay = models.DecimalField(verbose_name="支付金额", max_digits=7, decimal_places=2)
    start_time = models.DateTimeField(verbose_name="生效时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="失效时间", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
