from django.shortcuts import render, redirect
from django.db.models import RestrictedError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from user.models import Company, Project
from main.views import decorator_adds_user_information_log
from administrator.views import decorator_check_admin
from project.forms import ProjectForm


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def project_list(request, company_id):
    """Просмотр списка проектов компании"""
    try:
        projects = Project.objects.filter(company_id=company_id)
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404
    return render(request, "administrator/project/index.html", context={"projects": projects, "company": company})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def edit_project(request, company_id, id=None):
    """Добавление и изменение проекта"""
    if id:
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404
    else:
        project = None

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if not project:
                project = Project()
            project.name = form.cleaned_data['name']
            project.company = form.cleaned_data['company']
            project.save()
            return redirect(f'/project/list/{company_id}/')
        else:
            messages.error(request, "Invalid data")
    if project:
        form = ProjectForm(instance=project)
    else:
        form = ProjectForm(initial={'company': company})

    return render(request, "base_form.html", context={
        "form": form,
        "title": "edit project",
        "button_name": "save"
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def delete_project(request, company_id, id):
    """удаление проекта"""
    try:
        project = Project.objects.get(id=id)
        Company.objects.get(id=company_id)
    except (Project.DoesNotExist, Company.DoesNotExist):
        raise Http404
    if project:
        try:
            project.delete()
        except RestrictedError:
            messages.error(request, f"Can't delete project {project.name}")
    return redirect(f'/project/list/{company_id}')
