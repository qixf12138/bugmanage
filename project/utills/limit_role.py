from project.models import ProjectInfo


def project_limt(request, form, field="name"):
    """
    根据策略进行验证
    验证失败将错误信息添加到form.error里，将form.error放进字典并返回
    """
    # 获取项目创建策略
    policy = request.userinfo.policy
    project_count = ProjectInfo.objects.filter(creator=request.userinfo.user).count()
    if project_count >= policy.create_project:
        form.add_error(field, "项目创建已达上限")
        content = {"error_msg": form.errors}
        return content
