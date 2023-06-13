from django.template import Library

from project.models import ProjectInfo, ProjectUser

register = Library()


@register.inclusion_tag("inclusion/my_create_project_list.html")
def display_project(request):
    user = request.userinfo.user
    creator_projects = ProjectInfo.objects.filter(creator=user)
    join_projects = ProjectUser.objects.filter(user=user)
    return {"creator": creator_projects, "join": join_projects}


