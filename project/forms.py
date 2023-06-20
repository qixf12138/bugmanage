from django import forms
from crispy_forms.helper import FormHelper

from project.models import ProjectInfo, ProjectWikiInfo, ProjectFileInfo
from project.widgets import ColorRadioSelect
from utills.projectutills.forms import BootStrapModelsForm
from mdeditor.widgets import MDEditorWidget


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
    bootstarp_class_exclue = ["content"]

    class Meta:
        model = ProjectWikiInfo
        exclude = ["project", "depth"]

    content = forms.CharField(
        label="正文",
        # widget=MDEditorWidget()
        widget=forms.Textarea
    )

    def __init__(self, request, *args, **kargs):
        super().__init__(*args, **kargs)
        total_data_list = [("", "请选择")]
        data_list = ProjectWikiInfo.objects.filter(
            project_id=request.userinfo.project.id).values_list("id", "title")
        total_data_list += data_list
        self.fields['parent'].choices = total_data_list


class ProjectFileModelForm(BootStrapModelsForm):
    class Meta:
        model = ProjectFileInfo
        fields = ["name"]

