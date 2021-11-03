from django.forms import Form, DateField, ModelMultipleChoiceField, ChoiceField
from user.calendar import years
from user.models import User
from user import forms
from datetime import date

class SelectionForm(forms.SelectionForm):
    """Форма для выборки данных пользователей отдела за различные периоды времени"""
    users = ModelMultipleChoiceField(queryset=User.objects.filter(role=3))
    uploading_data = ChoiceField(label='Uploading data in the format', choices=((1, 'no format'), (2, '.csv'),
                                                                                (3, '.xlsx')))

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super(SelectionForm, self).__init__(*args, **kwargs)

        if self.department:
            self.fields['users'].queryset = User.objects.filter(role=3, department=self.department)

    def is_valid(self):
        valid = super(SelectionForm, self).is_valid()

        if not valid:
            return valid

        for user in self.cleaned_data['users']:
            if user.department != self.department:
                return False

        return True
