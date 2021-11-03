from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import Http404
from user.models import User
from administrator.models import UnregisteredUser
from administrator.forms import InvitationForm, ChangeUserForm
from main.views import decorator_adds_user_information_log


def decorator_check_admin(func):
    """"Декоратор для проверки роли пользователя"""
    def wrapped(request, **kwargs):
        if request.user.role == 1:
            return func(request, **kwargs)
        else:
            return redirect("/accounts/login")
    return wrapped


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def index(request):
    """Главная страница админа"""
    users = User.objects.exclude(role=1)
    return render(request, "administrator/index.html", context={'users': users})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def change_user(request, id):
    """Изменение отдела, блокировка или удаление пользователей"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404()
    if request.method == "POST":
        form = ChangeUserForm(request.POST)
        if form.is_valid():
            user.department = form.cleaned_data["department"]
            user.is_active = form.cleaned_data["is_active"]
            user.save()
            return redirect("/administrator/")
    else:
        form = ChangeUserForm(instance=user)
    return render(request, f"administrator/change-user.html", context={"form": form, "id": id})


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def delete_user(request, id):
    """удаление пользователя"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404
    if user:
        user.delete()
    return redirect('/administrator/')


@login_required
@decorator_adds_user_information_log
@decorator_check_admin
def invite_user(request):
    """Приглашение пользователя на регистрацию"""
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            found_email = User.objects.filter(email=form.cleaned_data["email"])
            if not found_email:
                user = UnregisteredUser()
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.department = form.cleaned_data["department"]
                user.post = form.cleaned_data["post"]
                user.role = form.cleaned_data["role"]
                while True:
                    code = user.generate_code()
                    if not UnregisteredUser.objects.filter(code=code):
                        user.code = code
                        break
                user.save()
                send_mail('Регистрация',
                          f'Уважаемый {user.first_name} {user.last_name}, приглашаем вас пройти регистрацию в приложении'
                          f' “Система учета рабочего времени сотрудников”.\nДля регистрации перейдите по ссылке '
                          f'http://127.0.0.1:8000/accounts/registration/\n'
                          f'Код доступа: {user.code}',
                          settings.EMAIL_HOST_USER,
                          [user.email])
                return redirect(index)
            else:
                messages.error(request, "Invalid data")
    else:
        form = InvitationForm()
    return render(request, "administrator/invitation.html", context={"form": form})
