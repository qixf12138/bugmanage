from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView

from bugmanage.views import BaseJsonView
from project.forms import ProjectWikiModelForm
from project.models import ProjectWikiInfo, ProjectInfo
from utills.datavalid.datavalid import id_number_vaild


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


class ProjectWiki(BaseJsonView):
    """
    Attributes
    -----------
    template_name：str
        html模板路径

    Method
    --------------
    valid_wiki_id（）验证wiki_id格式是否正确，如果正确并存在，返回wiki
    add_wiki_title_depth() 如果有父类ID，给传入的form.instance添加depth值（parent.depth+1），否则使用默认值1
    get_redirect_url（） 生成project_id wiki主页面或者wiki详情页面的url。通常用于添加，修改，删除后的跳转
    get() 获取wiki的主页信息或者是wiki的详情
    """
    template_name = "project/project_wiki.html"

    @staticmethod
    def valid_wiki_id(request, context, project_id):
        wiki_id = str(request.GET.get("wiki_id"))
        if id_number_vaild(wiki_id):
            wiki = ProjectWikiInfo.objects.filter(id=wiki_id, project_id=project_id).first()
            if wiki:
                context["wiki"] = wiki
                return wiki

    @staticmethod
    def get_redirect_url(project_id, wiki_id=None):
        if wiki_id:
            return "/project/"+str(project_id)+"/"+"wiki/?wiki_id=" + str(wiki_id)
        return "/project/"+str(project_id)+"/"+"wiki/"

    @staticmethod
    def add_wiki_title_depth(form):
        parent = form.cleaned_data.get("parent")
        if parent:
            form.instance.depth = parent.depth + 1

    def get(self, request, project_id):
        context = {}
        if not ProjectWiki.valid_wiki_id(request, context, project_id):
            pass
        return render(request, ProjectWiki.template_name, context)


class ProjectWikiAdd(View):
    """
    Attributes
    -----------
    template_name：str
        html模板路径

    Method
    --------------
    get() 获取添加wiki的表单页面
    post（）处理添加wiki的请求
    """

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
            # 给form的instance添加depth值
            ProjectWiki.add_wiki_title_depth(form)
            form.save()
        else:
            print(form.errors)

        return redirect(ProjectWiki.get_redirect_url(project_id))


class ProjectWikiAlter(BaseJsonView):
    """
    Attributes
    -----------
    template_name：str
        html模板路径

    Method
    --------------
    get() 获取添加wiki的修改表单页面，以及返回需要修改wiki的原本信息
    post（）处理修改wiki的请求
    """
    template_name = "project/project_wiki_alter.html"

    def get(self, request, project_id):
        context = {}
        wiki = ProjectWiki.valid_wiki_id(request, context, project_id)
        if not wiki:
            return self.error_response("请求格式不正确")
        form = ProjectWikiModelForm(instance=wiki, request=request)
        context["form"] = form
        return render(request, ProjectWikiAlter.template_name, context)

    def post(self, request, project_id):
        context = {}
        wiki = ProjectWiki.valid_wiki_id(request, context, project_id)
        if not wiki:
            return self.error_response("请求格式不正确")
        form = ProjectWikiModelForm(data=request.POST, instance=wiki, request=request)
        if form.is_valid():
            # 给form的instance添加depth值
            ProjectWiki.add_wiki_title_depth(form)
            form.save()
            return redirect(ProjectWiki.get_redirect_url(project_id, wiki.id))
        return self.error_response("数据验证失败")


# 删除wiki
def project_wiki_delete(request, project_id):
    wiki_id = request.GET.get("wiki_id")
    if id_number_vaild(wiki_id):
        wiki = ProjectWikiInfo.objects.filter(project_id=project_id, id=wiki_id)
        if wiki.exists():
            wiki.delete()
        else:
            return BaseJsonView.error_response("wiki不存在！")
    else:
        BaseJsonView.error_response("请求格式错误！")
    return render(request, ProjectWiki.template_name)


class ProjectWikiTitle(BaseJsonView):
    """
    Method
    --------------
    get() 根据project_id，获取相关所有标题
    """

    def get(self, request, project_id):
        # 中间件已经进行了项目验证，这里不再做额外验证
        wiki = ProjectWikiInfo.objects.filter(project_id=project_id).values()
        context = {"wiki": list(wiki)}
        return self.success_response_data(context)


class ProjectSettings(View):
    template_name = "project/project_settings.html"

    def get(self, request, project_id):
        return redirect(ProjectWiki.get_redirect_url(project_id))
