from django.test import SimpleTestCase

from project.forms import ProjectForm


class ProjectFormTest(SimpleTestCase):
    def test_name_field_label(self):
        form = ProjectForm()
        self.assertTrue(form.fields['name'].label is None or
                        form.fields['name'].label == 'Name')

    def test_company_field_label(self):
        form = ProjectForm()
        self.assertTrue(form.fields['company'].label is None or
                        form.fields['company'].label == 'Company')
