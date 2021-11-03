from django.test import SimpleTestCase

from administrator.forms import InvitationForm, ChangeUserForm


class InvitationFormTest(SimpleTestCase):
    def test_first_name_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['first_name'].label is None or
                        form.fields['first_name'].label == 'First name')

    def test_last_name_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['last_name'].label is None or
                        form.fields['last_name'].label == 'Last name')

    def test_email_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['email'].label is None or
                        form.fields['email'].label == 'Email')

    def test_department_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['department'].label is None or
                        form.fields['department'].label == 'Department')

    def test_post_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['post'].label is None or
                        form.fields['post'].label == 'Post')

    def test_role_field_label(self):
        form = InvitationForm()
        self.assertTrue(form.fields['role'].label is None or
                        form.fields['role'].label == 'Role')


class ChangeUserFormTest(SimpleTestCase):
    def test_department_field_label(self):
        form = ChangeUserForm()
        self.assertTrue(form.fields['department'].label is None or
                        form.fields['department'].label == 'Department')

    def test_is_active_field_label(self):
        form = ChangeUserForm()
        self.assertTrue(form.fields['is_active'].label is None or
                        form.fields['is_active'].label == 'Active')
