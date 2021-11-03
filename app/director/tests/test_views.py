from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Department, Company
from datetime import date

User = get_user_model()

class ViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user1 = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)
        cls.test_user2 = User.objects.create(password="", email="def@mail.ru", role=2, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.test_user1, cls.test_user2, cls.department, cls.company]:
            elem.delete()

    def test_check_access_index_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("director-page"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'director/index.html')

    def test_check_access_user_data_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("user-data", args=[self.test_user1.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'director/user_data.html')

    def test_1_invalid_user_id_user_data_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("user-data", args=[100]))
        self.assertEqual(resp.status_code, 404)

    def test_2_invalid_user_id_user_data_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("user-data", args=[self.test_user2.id]))
        self.assertEqual(resp.status_code, 404)

    def test_check_access_users_data_selection_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("users-data-selection"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'selection_form.html')

    def test_1_post_request_users_data_selection_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.post(reverse("users-data-selection"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'selection_form.html')

    def test_2_post_request_users_data_selection_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.post(reverse("users-data-selection"), data={
            "start_date": ["31/05/2021"],
            "end_date": ["01/06/2021"],
            "users": [f"{self.test_user1.id}"],
            "uploading_data": ["1"]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'director/users_data_selection.html')

    def test_3_post_request_users_data_selection_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.post(reverse("users-data-selection"), data={
            "start_date": ["31/05/2021"],
            "end_date": ["01/06/2021"],
            "users": [f"{self.test_user1.id}"],
            "uploading_data": ["2"]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")

    def test_4_post_request_users_data_selection_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.post(reverse("users-data-selection"), data={
            "start_date": ["31/05/2021"],
            "end_date": ["01/06/2021"],
            "users": [f"{self.test_user1.id}"],
            "uploading_data": ["3"]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/vnd.ms-excel")

    def test_checks_access_with_different_role_index_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("director-page"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_user_data_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("user-data", args=[1]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_users_data_selection_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("users-data-selection"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")