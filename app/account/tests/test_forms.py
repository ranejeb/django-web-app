from django.test import TestCase
from django.utils import timezone
from account.forms import LoginForm, RegisterForm

class FormsTestCase(TestCase):

    def test_checking_validity_login_form(self):
        self.assertTrue(LoginForm(data={
            "email": "abc@mail.ru",
            "password": "12345"
        }).is_valid())

    def test_1_checking_validity_register_form(self):
        self.assertTrue(RegisterForm(data={
            "password": "12345678",
            "password2": "12345678",
            "code": "12345"
        }).is_valid())

    def test_2_checking_validity_register_form(self):
        self.assertFalse(RegisterForm(data={
            "password": "12345678",
            "password2": "abc",
            "code": "12345"
        }).is_valid())

    def test_3_checking_validity_register_form(self):
        self.assertFalse(RegisterForm(data={
            "password": "12345",
            "password2": "12345",
            "code": "12345"
        }).is_valid())
