from django import forms

from user.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']
