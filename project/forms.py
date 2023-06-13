from django import forms
from crispy_forms.helper import FormHelper

from project.models import ProjectInfo, ProjectWikiInfo
from project.widgets import ColorRadioSelect
from utills.projectutills.forms import BootStrapModelsForm
from utills.projectutills.tools import get_now_data_str


class ProjectModelForm(BootStrapModelsForm):
    bootstarp_class_exclue = ["color"]

    class Meta:
        model = ProjectInfo
        fields = ["name", "color", "describe"]

    color = forms.ChoiceField(
        choices=ProjectInfo.COLOR_CHOICES,
        widget=ColorRadioSelect(),
        label="颜色",
    )


class ProjectCrispyForm(forms.ModelForm):
    class Meta:
        model = ProjectInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class ProjectWikiModelForm(BootStrapModelsForm):
    class Meta:
        model = ProjectWikiInfo
        exclude = ["project"]

    content = forms.CharField(
        label="正文",
        widget=forms.Textarea()
    )

    def __init__(self, request, *args, **kargs):
        super().__init__(*args, **kargs)
        total_data_list = [("", "请选择")]
        data_list = ProjectWikiInfo.objects.filter(
            project_id=request.userinfo.project.id).values_list("id", "title")
        total_data_list += data_list
        self.fields['parent'].choices = total_data_list

