from django.shortcuts import render, redirect
from django.db.models import RestrictedError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from user.models import Company
from main.views import decorator_adds_user_information_log
from administrator.views import decorator_check_admin
from company.forms import CompanyForm


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def company_list(request):
    """Просмотр списка компаний"""
    companies = Company.objects.all()
    return render(request, "administrator/company/index.html", context={"companies": companies})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def edit_company(request, id=None):
    """Добавление и изменение компании"""
    if id:
        try:
            company = Company.objects.get(id=id)
        except Company.DoesNotExist:
            raise Http404()
    else:
        company = None

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            if company:
                company.name = form.cleaned_data['name']
                company.save()
            else:
                form.save()
            return redirect('/company/list')
        else:
            messages.error(request, "Invalid data")
    form = CompanyForm(instance=company)

    return render(request, "base_form.html", context={
        "form": form,
        "title": "edit company",
        "button_name": "save"
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def delete_company(request, id):
    """удаление компании"""
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        raise Http404()
    if company:
        try:
            company.delete()
        except RestrictedError:
            messages.error(request, f"Can't delete company {company.name}")
    return redirect('/company/list/')
