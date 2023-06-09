
from django.db.models import F
from django.views import View
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse

from bugmanage.views import BaseJsonView
from project.utills.limit_role import project_limt
from user.models import UserInfo
from project.forms import ProjectModelForm
from project.models import ProjectUser, ProjectInfo
from utills.tencent.cos import COSBucket


class ProjectManage(View):
    """
    get():返回modal模态框的表单，返回登录的用户的信息
    """
    template_name = "project/project_list.html"

    def get(self, request):
        form = ProjectModelForm()
        user = request.session.get("user")
        if user:
            user = UserInfo.objects.filter(user=user).first()
        content = {
            "form": form,
            "user": user,
        }
        return render(request, ProjectManage.template_name, content)


class ProjectList(View):
    """
    get()返回并渲染 星标项目 （ProjectUser）和 我创建的项目 （ProjectInfo） 两个模板
    """
    template_name = "project/project_list_panel_card.html"

    def get(self, request):
        user_id = request.session.get("id")
        join_projects = ProjectUser.objects.filter(user=user_id)
        creator_projects = ProjectInfo.objects.filter(creator_id=user_id)
        content = {"star": [], "join": [], "creator": []}
        for project in join_projects:
            project.project.user_num = ProjectUser.objects.filter(project_id=project.project_id).count()
            if project.star_mark:
                content["star"].append(project.project)
            else:
                content["join"].append(project)

        for project in creator_projects:
            project.user_num = ProjectUser.objects.filter(project_id=project.id).count()
            if project.star_mark:
                content["star"].append(project)
            else:
                content["creator"].append(project)
        # content = {
        #         "join_projects": join_projects,
        #         "creator_projects": creator_projects,
        # }
        return render(request, ProjectList.template_name, content)


class ProjectAdd(BaseJsonView):
    """
    post（）：新增请求
            form数据验证成功，返回status:200。
            form数据验证失败，返回status:400 + error_msg: form.errors的错误信息
    """
    def post(self, request):
        content = {}
        form = ProjectModelForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            # 增加项目创建上限验证
            is_limit_msg = project_limt(request, form)
            if is_limit_msg:
                return self.error_response_data(is_limit_msg)
            cos = COSBucket()
            bucket_name = cos.create_bucket()
            # 获取request内的用户名，创建时自动填写创建者、创建时间
            form.instance.creator_id = request.userinfo.user.id
            form.instance.bucket = bucket_name
            form.save()
            # project = form.save()
            # star_mark = form.instance.star_mark
            # 将创建人加入到项目关系表中
            # ProjectUser.objects.create(user_id=user, project=project, star_mark=star_mark)
        else:
            content["error_msg"] = form.errors
            return self.error_response_data(content)
        return self.success_response()


class ProjectAlter(BaseJsonView):
    """
    修改项目
    get(): 成功获取返回ProjectInfo的json对象
           失败返回status:400json对象

    post():成功保存信息到数据库，返回status:200json对象，由前端继续请求/project/list/获取最新信息
           失败返回status:400json对象
    """

    def get(self, request):
        content = {}

        project_id = request.GET.get("id")
        # 根据参数id获取要修改project
        project = ProjectInfo.objects.filter(id=project_id)

        # 如果存在返回该project的数据信息
        if project.exists():
            content["project"] = model_to_dict(project.first())
            return self.success_response_data(content)
        else:
            return self.error_response("项目不存在！")

    def post(self, request):
        content = {}
        # 根据参数id获取要修改project
        project_id = request.POST.get("id")
        project = ProjectInfo.objects.filter(id=project_id)

        # 如果存在则创建modelform对象
        if project.exists():
            form = ProjectModelForm(data=request.POST, instance=project.first())
            # 验证form数据，通过保存，返回html，错误返回json字符串
            if form.is_valid():
                project = form.save()
                # 修改ProjectUser的星标，试项目星标与关系星标保持一致。
                # print(project.star_mark)
                # project_to_user = ProjectUser.objects.filter(project=project, user=project.creator).first()
                # project_to_user.star_mark = project.star_mark
                # project_to_user.save()
                return self.success_response()
            else:
                content["error_msg"] = form.errors
        else:
            return self.error_response("项目不存在！")
        return self.error_response_data(content)


class ProjectStarMark(BaseJsonView):
    """
    修改项目星标
    get()：根据session中的用户名查询用户，验证成功返回status:200成功标志
           验证失败返回status:400标志
    """
    def get(self, request):
        # 查询session内的用户是否有效
        user = request.session.get("user")
        user = UserInfo.objects.filter(user=user).first()
        if user:
            # 根据project_id和user查询数来的数据取反,如果没有找到数据，返回0
            project_id = request.GET.get("project_id")
            create_project = ProjectInfo.objects.filter(id=project_id,
                                                        creator=user).update(star_mark=~F('star_mark'))
            # 如果返回0,则不是项目的创建者，去项目参与关系表里找
            if not create_project:
                join_project = ProjectUser.objects.filter(project_id__in=(project_id,),
                                                          user=user).update(star_mark=~F('star_mark'))
                if not join_project:
                    return self.error_response("未找到相关项目信息")
            return self.success_response()
        return self.error_response("用户无效")


