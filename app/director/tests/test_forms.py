from django.test import TestCase
from director.forms import SelectionForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from user.models import Department, Company
from datetime import date

User = get_user_model()

class FormsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user1 = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                             first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                             date_joined=timezone.now(), post="user", department=cls.department)
        cls.test_user2 = User.objects.create(password="", email="def@mail.ru", role=3, is_superuser=True,
                                             first_name="def", last_name="def", is_staff=1, is_active=1,
                                             date_joined=timezone.now(), post="user", department=cls.department)
        cls.test_user3 = User.objects.create(password="", email="ghi@mail.ru", role=3, is_superuser=True,
                                             first_name="ghi", last_name="ghi", is_staff=1, is_active=1,
                                             date_joined=timezone.now(), post="user")

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.test_user1, cls.test_user2, cls.test_user3, cls.department, cls.company]:
            elem.delete()

    def test_create_selection_form(self):
        users = SelectionForm(department=self.department).fields["users"].queryset
        self.assertTrue(self.test_user1 in users)
        self.assertTrue(self.test_user2 in users)
        self.assertTrue(self.test_user3 not in users)

    def test_1_checking_validity_selection_form(self):
        self.assertTrue(SelectionForm(data={
            "end_date": date.today(),
            "start_date": date(2021, 5, 31),
            "users": [self.test_user1, self.test_user2],
            "uploading_data": 1
        }, department=self.department).is_valid())

    def test_2_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "end_date": date(2021, 5, 31),
            "start_date": date.today(),
            "users": [self.test_user1, self.test_user2],
            "uploading_data": 1
        }, department=self.department).is_valid())

    def test_3_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "end_date": date.today(),
            "start_date": date.today(),
            "users": [self.test_user1, self.test_user2],
            "uploading_data": 1
        }, department=self.department).is_valid())

    def test_4_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "end_date": date(1200, 5, 20),
            "start_date": date.today(),
            "users": [self.test_user1, self.test_user2],
            "uploading_data": 1
        }, department=self.department).is_valid())

    def test_5_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "end_date": date(2021, 5, 31),
            "start_date": date.today(),
            "users": [self.test_user1, self.test_user2],
            "uploading_data": 5
        }, department=self.department).is_valid())

    def test_6_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "end_date": date(2021, 5, 31),
            "start_date": date.today(),
            "users": [self.test_user1, self.test_user2, self.test_user3],
            "uploading_data": 1
        }, department=self.department).is_valid())