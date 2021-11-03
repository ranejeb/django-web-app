from django.forms import ModelForm, Form, IntegerField, CharField, DateField
from django import forms
from user.models import Task, User
from user.calendar import years, months
from datetime import date


class ChangeDataUserForm(ModelForm):
    """Форма для редактирования данных пользователя"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ChangePasswordUserForm(Form):
    """Форма для смены пароля пользователя"""
    old_password = forms.CharField(label="old password", widget=forms.PasswordInput)
    password = forms.CharField(label="new password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="repeat password", widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords don't match")
        return cd['password2']


class CalendarForm(Form):
    """Форма, проверяющая год, месяц календаря"""
    year = IntegerField(required=False)
    month = CharField(required=False)

    def is_valid(self):
        valid = super(CalendarForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['year'] not in years or self.cleaned_data['month'] not in months:
            return False

        return True


class TaskForm(ModelForm):
    """Форма для добавления, редактирования занятия"""
    class Meta:
        model = Task
        fields = ['time_worked', 'description', 'project']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['project'].queryset = user.department.project.all()

class SelectionForm(Form):
    """Форма для выборки заданий за различные периоды времени"""
    start_date = DateField(label='From', input_formats=['%d/%m/%Y'])
    end_date = DateField(label='To', input_formats=['%d/%m/%Y'])

    def is_valid(self):
        valid = super(SelectionForm, self).is_valid()

        if not valid:
            return valid

        get_start_date, get_end_date = self.cleaned_data['start_date'], self.cleaned_data['end_date']

        if get_start_date >= get_end_date or get_start_date.year < years[-1] or get_end_date > date.today():
            return False

        return True
