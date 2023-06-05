from django import template
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo
from project.models import ProjectInfo, UserJoinProjectInfo
from project.forms import ProjectModelForm
from utills.projectutills.tools import get_now_data_str


def project_list(request):
    if request.method == "GET":
        form = ProjectModelForm()
        content = {"form": form}
        # 获取session里面的用户名，根据用户名查询出创建的项目
        user = request.session.get("user")
        user = UserInfo.objects.filter(user=user).first()
        if user:
            # 返回用户的参与的项目
            #projects = UserJoinProjectInfo.objects.filter(user=user)
            # projects = UserJoinProjectInfo.objects.filter(user=user, star_mark=False)
            user_projects = UserJoinProjectInfo.objects.filter(user=user)
            # 根据查询出的项目对象，查询出项目的参与人数
            for project in user_projects:
                project.user_num = UserJoinProjectInfo.objects.filter(project=project.project).count()
            content["user"] = user
            #content["projects"] = projects
            # 返回用户星标项目
            # 返回用户星标项目
            # 返回用户星标项目 # 返回用户星标项目(未完成)
            content["user_project"] = user_projects

    elif request.method == "POST":
        content = {}
        form = ProjectModelForm(data=request.POST)
        if form.is_valid():
            print("验证通过")
            # 获取session内的用户名，创建时自动填写创建者、创建时间（暂时没有写使用空间，后续考虑专门编写一个方法）
            user = request.session.get("user")
            user = UserInfo.objects.filter(user=user).first()
            create_time = get_now_data_str()
            form.instance.user = user
            form.instance.create_time = create_time
            project = form.save()
            # 将创建人加入到项目关系表中
            UserJoinProjectInfo.objects.create(user=project.user, project=project)
            content["status"] = 200
        else:
            content["error_msg"] = form.errors
        return JsonResponse(content)
    else:
        return JsonResponse("请求错误！")
    return render(request, "project/list.html", content)


@csrf_exempt
def project_alter(request):
    content = {}
    # 返回要修改的项目数据
    if request.method == "GET":
        project_id = request.GET.get("id")
        project = ProjectInfo.objects.filter(id=project_id)
        if project.exists():
            content["status"] = 200
            content["project"] = model_to_dict(project.first())
        else:
            content["status"] = 400
    elif request.method == "POST":
        project_id = request.POST.get("id")
        project = ProjectInfo.objects.filter(id=project_id)
        print(project)
        if project.exists():
            form = ProjectModelForm(data=request.POST, instance=project.first())
            print(form)
            if form.is_valid():
                form.save()
                content["status"] = 200
            else:
                content["errno_msg"] = form.errors
        else:
            content["status"] = 400
    else:
        content["status"] = 400
    return JsonResponse(content)


def project_star_mark(request):
    if request.method == "GET":
        user = request.session.get("user")
        user = UserInfo.objects.filter(user=user).first()
        if user:
            project_id = request.GET.get("project_id")
            project = UserJoinProjectInfo.objects.filter(project_id=project_id, user=user)
            if project.exists():
                project = project.first()
                print(project.star_mark)
                project.star_mark = not project.star_mark
                print(project.star_mark)
                project.save()
                content = {"status": 200}
                user_project = UserJoinProjectInfo.objects.filter(user=user)
                content["user_project"] = user_project
            else:
                content = {"status": 400}
    else:
        content = {"status": 400}
    return render(request, "project/ajax_list_panel.html", content)

