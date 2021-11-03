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

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.test_user, cls.department, cls.company]:
            elem.delete()

    def test_1_check_access_index_view(self):
        self.client.force_login(self.test_user)
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("user-page"))

    def test_2_check_access_index_view(self):
        self.test_user.role = 2
        self.test_user.save()
        self.client.force_login(self.test_user)
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("director-page"))

    def test_3_check_access_index_view(self):
        self.test_user.role = 1
        self.test_user.save()
        self.client.force_login(self.test_user)
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("administrator-page"))

    def test_4_check_access_index_view(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login/?next=/")
