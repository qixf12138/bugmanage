from django import forms
from crispy_forms.helper import FormHelper
from project.models import ProjectInfo
from utills.projectutills.forms import BootStrapModelsForm
from utills.projectutills.tools import get_now_data_str


class ProjectModelForm(BootStrapModelsForm):
    class Meta:
        model = ProjectInfo
        fields = ["name", "color", "describe"]


class ProjectCrispyForm(forms.ModelForm):
    class Meta:
        model = ProjectInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
