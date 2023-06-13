from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView

from bugmanage.views import BaseJsonView
from project.forms import ProjectWikiModelForm
from project.models import ProjectWikiInfo, ProjectInfo


class ProjectOverView(View):
    template_name = "project/project_overview.html"

    def get(self, request, project_id):
        return render(request, ProjectOverView.template_name)


class ProjectIssue(View):
    template_name = "project/project_issue.html"

    def get(self, request, project_id):
        print(request.path)
        return render(request, ProjectIssue.template_name)


class ProjectAnalyze(View):
    template_name = "project/project_analyz.html"

    def get(self, request, project_id):
        return render(request, ProjectAnalyze.template_name)


class ProjectFile(View):
    template_name = "project/project_file.html"

    def get(self, request, project_id):
        return render(request, ProjectFile.template_name)


class ProjectIssue(View):
    template_name = "project/project_issue.html"

    def get(self, request, project_id):
        return render(request, ProjectIssue.template_name)


class ProjectWiki(View):
    template_name = "project/project_wiki.html"

    def get(self, request, project_id):
        return render(request, ProjectWiki.template_name)


class ProjectWikiDesc(View):
    template_name = "project/project_wiki.html"

    def get(self, request, project_id, wiki_id):
        form = ProjectWikiModelForm(request=request)
        wiki = ProjectWikiInfo.objects.filter(id=wiki_id).first()
        if wiki:
            context = {"wiki": wiki}
        return render(request, ProjectWiki.template_name, context)


class ProjectWikiAdd(View):
    template_name = "project/project_wiki_add.html"

    def get(self, request, project_id):
        form = ProjectWikiModelForm(request=request)
        return render(request, ProjectWikiAdd.template_name, {"form": form})

    def post(self, request, project_id):
        project = ProjectInfo.objects.filter(id=project_id).first()
        if not project:
            return redirect("/project/" + str(project_id) + "/" + "wiki/")
        form = ProjectWikiModelForm(data=request.POST, request=request)
        if form.is_valid():
            form.instance.project = project
            form.save()
        else:
            print(form.errors)
        return redirect("/project/"+str(project_id)+"/"+"wiki/")


class ProjectWikiAlter(View):
    template_name = "project/project_wiki_alter.html"

    def get(self, request, project_id, wiki_id):
        wiki = ProjectWikiInfo.objects.filter(project_id=project_id, id=wiki_id).first()
        if wiki:
            form = ProjectWikiModelForm(instance=wiki, request=request)
        return render(request, ProjectWikiAlter.template_name, {"form": form})

    def post(self, request, project_id, wiki_id):
        wiki = ProjectWikiInfo.objects.filter(project_id=project_id, id=wiki_id).first()
        if not wiki:
            pass
        form = ProjectWikiModelForm(data=request.POST, instance=wiki, request=request)
        if form.is_valid():
            form.save()
            return redirect("/project/" + str(project_id) + "/wiki/" + str(wiki_id) + "/")


def project_wiki_delete(request, project_id, wiki_id):
    wiki = ProjectWikiInfo.objects.filter(project_id=project_id, id=wiki_id)
    if wiki.exists():
        wiki.delete()
    return render(request, ProjectWikiDesc.template_name)





class ProjectWikiTitle(BaseJsonView):
    def get(self, request, project_id):
        # 中间件已经进行了项目验证，这里不再做额外验证
        wiki = ProjectWikiInfo.objects.filter(project_id=project_id).order_by("id").values()
        context = {"wiki": list(wiki)}
        return self.success_response_data(context)


class ProjectSettings(View):
    template_name = "project/project_settings.html"

    def get(self, request, project_id):
        return render(request, ProjectSettings.template_name)
