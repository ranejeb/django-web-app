from django.test import TestCase
from django.urls import reverse
from user.models import User, Department, Company
from django.utils import timezone
from administrator.models import UnregisteredUser


class ViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                            first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                            date_joined=timezone.now(), post="user", department=cls.department)
        cls.test_user.set_password("12345")
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.test_user, cls.department, cls.company]:
            elem.delete()

    def test_check_access_login_view(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base_form.html")

    def test_1_post_request_login_view(self):
        resp = self.client.post(reverse("login"), data={
            "email": ["abc@mail.ru"],
            "password": ["12345"],
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("user-page"))

    def test_2_post_request_login_view(self):
        self.test_user.role = 2
        self.test_user.save()
        resp = self.client.post(reverse("login"), data={
            "email": ["abc@mail.ru"],
            "password": ["12345"],
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("director-page"))

    def test_3_post_request_login_view(self):
        self.test_user.role = 1
        self.test_user.save()
        resp = self.client.post(reverse("login"), data={
            "email": ["abc@mail.ru"],
            "password": ["12345"],
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("administrator-page"))

    def test_4_post_request_login_view(self):
        resp = self.client.post(reverse("login"), data={
            "email": ["abc@mail.ru"],
            "password": ["123"],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base_form.html")

    def test_5_post_request_login_view(self):
        resp = self.client.post(reverse("login"), data={
            "email": ["ac@mail.ru"],
            "password": ["12345"],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base_form.html")

    def test_1_check_access_logout_view(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("login"))

    def test_2_check_access_logout_view(self):
        resp = self.client.get(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login/?next=/accounts/logout/")

    def test_check_access_registration_view(self):
        resp = self.client.get(reverse("registration"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base_form.html")

    def test_1_post_request_registration_view(self):
        resp = self.client.post(reverse("registration"), data={
            "code": ["12345"],
            "password": ["12345678"],
            "password2": ["12345678"]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base_form.html")

    def test_2_post_request_registration_view(self):
        UnregisteredUser.objects.create(code="12345", first_name="abc", last_name="abc", email="ads@mail.ru",
                                        post="ads", department=self.department)
        resp = self.client.post(reverse("registration"), data={
            "code": ["12345"],
            "password": ["12345678"],
            "password2": ["12345678"]
        })
        self.assertEqual(str(User.objects.get(email="ads@mail.ru")), "abc abc")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")