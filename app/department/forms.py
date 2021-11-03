from django import forms

from user.models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'project']
