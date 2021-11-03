from django.test import TestCase
from django.utils import timezone
from user.models import User, Department, Company, Project
from user.forms import ChangeDataUserForm, ChangePasswordUserForm, CalendarForm, TaskForm, SelectionForm
from datetime import date


class ChangeDataUserFormTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user")

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()

    def test_checking_validity_change_data_user_form(self):
        self.assertTrue(ChangeDataUserForm(data={
            "first_name": "abc",
            "last_name": "abc",
        }).is_valid())


class TaskFormTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)
        cls.project1 = Project.objects.create(name="dsg", company=cls.company)
        cls.project2 = Project.objects.create(name="dfg", company=cls.company)
        cls.test_user.department.project.add(cls.project1)

    @classmethod
    def tearDownClass(cls):
        cls.test_user.department.project.clear()
        for elem in [cls.project1, cls.project2, cls.test_user, cls.department, cls.company]:
            elem.delete()

    def test_create_task_form(self):
        projects = TaskForm(user=self.test_user).fields["project"].queryset
        self.assertIn(self.project1, projects)
        self.assertNotIn(self.project2, projects)

    def test_1_checking_validity_task_form(self):
        self.assertTrue(TaskForm(data={
            "time_worked": 120,
            "description": "abc",
            "project": self.project1
        }, user=self.test_user).is_valid())

    def test_2_checking_validity_task_form(self):
        self.assertFalse(TaskForm(data={
            "time_worked": 120,
            "description": "abc",
            "project": self.project2
        }, user=self.test_user).is_valid())

    def test_3_checking_validity_task_form(self):
        self.assertFalse(TaskForm(data={
            "time_worked": 120,
            "description": "abc",
            "project": None
        }, user=self.test_user).is_valid())


class FormsTestCase(TestCase):

    def test_1_checking_validity_change_password_user_form(self):
        form = ChangePasswordUserForm(data={
            "old_password": "12345",
            "password": "abc",
            "password2": "abc"
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_password2(), "abc")

    def test_2_checking_validity_change_password_user_form(self):
        self.assertFalse(ChangePasswordUserForm(data={
            "old_password": "12345",
            "password": "abc",
            "password2": "def"
        }).is_valid())

    def test_1_checking_validity_calendar_form(self):
        self.assertTrue(CalendarForm(data={
            "year": date.today().year,
            "month": "May"
        }).is_valid())

    def test_2_checking_validity_calendar_form(self):
        self.assertFalse(CalendarForm(data={
            "year": 2001,
            "month": "May"
        }).is_valid())

    def test_3_checking_validity_calendar_form(self):
        self.assertFalse(CalendarForm(data={
            "year": date.today().year,
            "month": "abc"
        }).is_valid())

    def test_4_checking_validity_calendar_form(self):
        self.assertFalse(CalendarForm(data={
            "year": date.today().year + 1,
            "month": "May"
        }).is_valid())

    def test_1_checking_validity_selection_form(self):
        self.assertTrue(SelectionForm(data={
            "start_date": date(2021, 5, 31),
            "end_date": date.today()
        }).is_valid())

    def test_2_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "start_date": date.today(),
            "end_date": date.today()
        }).is_valid())

    def test_3_checking_validity_selection_form(self):
        self.assertFalse(SelectionForm(data={
            "start_date": date(2001, 5, 20),
            "end_date": date.today()
        }).is_valid())
