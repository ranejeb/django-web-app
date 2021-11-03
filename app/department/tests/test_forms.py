from django.test import SimpleTestCase

from department.forms import DepartmentForm


class CompanyFormTest(SimpleTestCase):
    def test_name_field_label(self):
        form = DepartmentForm()
        self.assertTrue(form.fields['name'].label is None or
                        form.fields['name'].label == 'Name')

    def test_project_field_label(self):
        form = DepartmentForm()
        self.assertTrue(form.fields['project'].label is None or
                        form.fields['project'].label == 'Project')
