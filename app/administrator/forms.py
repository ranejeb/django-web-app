from django import forms

from administrator.models import UnregisteredUser
from user.models import User, Company


class InvitationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=((1, 'admin'), (2, 'director'), (3, 'user')))

    class Meta:
        model = UnregisteredUser
        fields = ['first_name', 'last_name', 'email', 'department', 'post']


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['department', 'is_active']
