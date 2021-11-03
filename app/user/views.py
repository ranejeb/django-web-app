from django.http import Http404
from django.shortcuts import render, redirect
from user.forms import ChangeDataUserForm, CalendarForm, ChangePasswordUserForm, TaskForm, SelectionForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from datetime import date
from user.calendar import get_all_weeks_month, years, months
from user.models import Task
from django.urls import reverse_lazy
from main.views import decorator_adds_user_information_log


def decorator_check_user(func):
    """"Декоратор для проверки роли пользователя"""
    def wrapped(request, **kwargs):
        if request.user.role == 3:
            return func(request, **kwargs)
        else:
            return redirect("/accounts/login")
    return wrapped


def decorator_check_date(func):
    """Декоратор для проверки даты"""
    def wrapped(request, year, month, day):
        if year in years and month in [i for i in range(1, 13)] and 1 <= day <= 31:
            try:
                return func(request, year, month, day)
            except ValueError:
                raise Http404()
        else:
            raise Http404()
    return wrapped


def decorator_handles_task_DoesNotExist(func):
    """Декоратор, обрабатывайщий исключение Task.DoesNotExist"""
    def wrapped(request, **kwargs):
        try:
            return func(request, **kwargs)
        except Task.DoesNotExist:
            raise Http404()
    return wrapped


@login_required
@decorator_adds_user_information_log
@decorator_check_user
def index(request):
    """Главная страница пользователя"""
    today = date.today()

    if request.method == "POST":
        form = CalendarForm(request.POST)
        if form.is_valid():
            year, month = form.cleaned_data["year"], months.index(form.cleaned_data["month"]) + 1
        else:
            year, month = today.year, today.month
    else:
        year, month = today.year, today.month

    weeks = get_all_weeks_month(year, month)

    return render(request, "user/main/index.html", context={
        "years": years,
        "current_year": year,
        "current_month": month,
        "months": months,
        "weeks": weeks,
        "today": today,
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_user
@decorator_check_date
def tasks(request, year, month, day):
    """Список заданий на определенный день"""
    get_date = date(year, month, day)
    return render(request, "user/tasks/index.html", context={
        "date": get_date,
        "tasks": Task.objects.filter(user__id=request.user.id, date=get_date),
    })


@login_required
@decorator_adds_user_information_log
def change_password_user(request):
    """Смена пароля пользователя"""
    if request.method == "POST":
        form = ChangePasswordUserForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            if not check_password(old_password, request.user.password):
                messages.error(request, "wrong old password!")
                return render(request, "form.html", context={
                    "form": form,
                    "title": "Change password",
                    "url_back": reverse_lazy('user-page'),
                    "button_name": "Edit"
                })
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            return redirect("/accounts/login")
    else:
        form = ChangePasswordUserForm()
    return render(request, "form.html", context={
        "form": form,
        "title": "Change password",
        "url_back": reverse_lazy("home"),
        "button_name": "Edit"
    })


@login_required
@decorator_adds_user_information_log
def change_data_user(request):
    """Редактирование данных пользователя"""
    if request.method == "POST":
        form = ChangeDataUserForm(request.POST)
        if form.is_valid():
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.save()
            return redirect("/")
        else:
            messages.error(request, "Invalid data")
    form = ChangeDataUserForm(instance=request.user)
    return render(request, "form.html", context={
        "form": form,
        "title": "Change data",
        "url_back": reverse_lazy('home'),
        "button_name": "Edit"
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_user
@decorator_check_date
def create_task(request, year, month, day):
    """Добавление задания"""
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            Task.objects.create(**{
                "project": form.cleaned_data["project"],
                "time_worked": form.cleaned_data["time_worked"],
                "description": form.cleaned_data["description"],
                "date": date(year, month, day),
                "user": request.user,
            })
            return redirect(tasks, year, month, day)
        else:
            messages.error(request, "Invalid data")
    return render(request, "form.html", context={
        "form": TaskForm(user=request.user),
        "title": "Create task",
        "url_back": reverse_lazy('list-tasks', args=[year, month, day]),
        "button_name": "Create",
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_user
@decorator_handles_task_DoesNotExist
def edit_task(request, task_id):
    """Редактирование задания"""
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            Task.objects.filter(id=task_id, user=request.user).update(**{
                "project": form.cleaned_data["project"],
                "time_worked": form.cleaned_data["time_worked"],
                "description": form.cleaned_data["description"],
            })
            task = Task.objects.get(id=task_id, user=request.user)
            return redirect(tasks, task.date.year, task.date.month, task.date.day)
        else:
            messages.error(request, "Invalid data")
    task = Task.objects.get(id=task_id)
    return render(request, "form.html", context={
        "form": TaskForm(user=request.user, instance=Task.objects.get(id=task_id, user=request.user)),
        "title": "Edit task",
        "url_back": reverse_lazy('list-tasks', args=[task.date.year, task.date.month, task.date.day]),
        "button_name": "Edit",
    })


@login_required
@decorator_adds_user_information_log
@decorator_check_user
@decorator_handles_task_DoesNotExist
def delete_task(request, task_id):
    """Удаление задания"""
    task = Task.objects.get(id=task_id, user=request.user)
    year, month, day = task.date.year, task.date.month, task.date.day
    task.delete()
    return redirect(tasks, year, month, day)


@login_required
@decorator_adds_user_information_log
@decorator_check_user
def select_tasks(request):
    """Выборка заданий за различные периоды времени"""
    if request.method == "POST":
        form = SelectionForm(request.POST)
        if form.is_valid():
            return render(request, "user/tasks/list_tasks.html", context={
                "tasks": Task.objects.filter(user=request.user).exclude(
                    date__gt=form.cleaned_data["end_date"]).exclude(date__lt=form.cleaned_data["start_date"])
            })
        else:
            messages.error(request, "Invalid data")
    return render(request, "selection_form.html", context={
        "form": SelectionForm(),
        "title": "Selection form",
        "url_back": reverse_lazy('user-page'),
        "button_name": "Execute",
    })