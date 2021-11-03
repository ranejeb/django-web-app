from django.test import SimpleTestCase

from company.forms import CompanyForm


class CompanyFormTest(SimpleTestCase):
    def test_name_field_label(self):
        form = CompanyForm()
        self.assertTrue(form.fields['name'].label is None or
                        form.fields['name'].label == 'Name')
