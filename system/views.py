from django.forms import model_to_dict
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from project.forms import ProjectModelForm
from project.models import ProjectInfo, ProjectUser
from user.models import UserInfo


# def project_manage(request):
#     content = {}
#     if request.method == "GET":
#         form = ProjectModelForm()
#         content["form"] = form
#         # 获取session里面的用户名，根据用户名查询出创建的项目
#         user = request.session.get("user")
#         user = UserInfo.objects.filter(user=user).first()
#         if user:
#             content["user"] = user
#     else:
#         return JsonResponse("错误请求")
#     return render(request, "system/project_list.html", content)


class ProjectManage(View):
    """
    get():返回modal模态框的表单，返回登录的用户的信息
    """
    templates_name = "system/project_list.html"

    def get(self, request):
        form = ProjectModelForm()
        user = request.session.get("user")
        if user:
            user = UserInfo.objects.filter(user=user).first()
        content = {
            "form": form,
            "user": user,
        }
        return render(request, ProjectManage.templates_name, content)


class ProjectList(View):
    """
    get()返回并渲染 星标项目 （ProjectUser）和 我创建的项目 （ProjectInfo） 两个模板
    """
    templates_name = "system/project_list_panel_card.html"

    def get(self, request):
        user_id = request.session.get("id")
        user_projects = ProjectUser.objects.filter(user=user_id)
        my_create_projects = ProjectInfo.objects.filter(creator_id=user_id)
        content = {
                "user_projects": user_projects,
                "my_create_projects": my_create_projects,
        }
        return render(request, ProjectList.templates_name, content)


class ProjectAdd(View):
    """
    post（）：新增请求
            form数据验证成功，返回status:200。
            form数据验证失败，返回status:400 + error_msg: form.errors的错误信息
    """
    def post(self, request):
        content = {}
        form = ProjectModelForm(data=request.POST)
        if form.is_valid():
            # 获取session内的用户名，创建时自动填写创建者、创建时间（暂时没有写使用空间，后续考虑专门编写一个方法）
            user = request.session.get("id")
            form.instance.creator_id = user
            project = form.save()
            star_mark = form.instance.star_mark
            # 将创建人加入到项目关系表中
            ProjectUser.objects.create(user_id=user, project=project, star_mark=star_mark)
            content["status"] = 200
        else:
            content["status"] = 400
            content["error_msg"] = form.errors
        return JsonResponse(content)


class ProjectAlter(View):
    """
    修改项目
    get(): 成功获取返回ProjectInfo的json对象
           失败返回status:400json对象

    post():成功保存信息到数据库，返回status:200json对象，由前端继续请求/project/list/获取最新信息
           失败返回status:400json对象
    """
    templates_name = "system/project_list_panel_card.html"

    def get(self, request):
        content = {}

        project_id = request.GET.get("id")
        # 根据参数id获取要修改project
        project = ProjectInfo.objects.filter(id=project_id)

        #如果存在返回该project的数据信息
        if project.exists():
            content["status"] = 200
            content["project"] = model_to_dict(project.first())
        else:
            content["status"] = 400
        return JsonResponse(content)

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
                print(project.star_mark)
                project_to_user = ProjectUser.objects.filter(project=project, user=project.creator).first()
                project_to_user.star_mark = project.star_mark
                project_to_user.save()
                # 设置标识成功
                content['status'] = 200
                return JsonResponse(content)
            else:
                content["error_msg"] = form.errors
        else:
            content["status"] = 400
        return JsonResponse(content)


class ProjectStarMark(View):
    """
    修改项目星标
    get()：根据session中的用户名查询用户，验证成功返回status:200成功标志
           验证失败返回status:400标志
    """
    def get(self, request):
        user = request.session.get("user")
        user = UserInfo.objects.filter(user=user).first()
        if user:
            project_id = request.GET.get("project_id")
            project_user = ProjectUser.objects.filter(project_id=project_id, user=user)
            project = ProjectInfo.objects.filter(id=project_id, creator=user)
            print(project_user)
            print(project)
            # 同时将ProjectUser和ProjectInfo两个表对应的项目进行星标
            if project_user.exists() and project.exists():
                project_user = project_user.first()
                project = project.first()
                project_user.star_mark = not project_user.star_mark
                project.star_mark = project_user.star_mark
                project_user.save()
                project.save()
                content = {"status": 200}
                print("木有错")
                return JsonResponse(content)
        print("戳错啦")
        content = {"status": 400}
        return JsonResponse(content)
