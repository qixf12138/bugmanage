from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from user.models import UserInfo
from utills.projectutills.encrypt import md5
from utills.projectutills.forms import BootStrapModelsForm


class RegisterModelForm(BootStrapModelsForm):
    """
    用户注册表单
    (目前没有对手机号进行唯一限制，从redis获取验证码后并没有将他删除，所以有效期内，一个手机号可以注册多个账号)
    """
    password = forms.CharField(
        label="密码",
        # render_value=True 在输入信息有误时可以返回错误信息
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    mobile_phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$",
                                   "手机号格式错误")],
    )

    code = forms.CharField(
        label="验证码",
        validators=[RegexValidator(r"^\d{6}$", "验证码格式错误,请输入6位数字的验证码")]
    )

    def clean_confirm_password(self):
        # 判断md5加密后“密码”与“确认密码”的内容是否一致
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        if confirm_pwd != pwd:
            raise ValidationError("密码不一致")
        else:
            return confirm_pwd

    def clean_password(self):
        # 将前台获取的密码转换为md5加密后的密码
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    class Meta:
        model = UserInfo
        fields = ["user",  "gender", "password", "confirm_password",
                  "email", "mobile_phone", "code"]

