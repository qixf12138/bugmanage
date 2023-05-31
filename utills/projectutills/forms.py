"""
作为appname。forms的父类，为所有子类生成的表单添加样式
class="form-control"
placeholder=field.label
"""

from django import forms


class NormalForm:
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # 循环所有插件，添加form-control属性
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control",
                                      "placeholder": field.label}


class BootStrapForm(NormalForm, forms.Form):
    """
    继承Form类,用于自动生成表单
    """
    pass


class BootStrapModelsForm(NormalForm, forms.ModelForm):
    """
    继承ModelForm类，用于自动生成表单
    """
    pass

