from django.test import TestCase
from user.models import User, Company, Department, Project, Task
from django.utils import timezone
from django.db.utils import IntegrityError
from datetime import date

class ModelsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                         first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                         date_joined=timezone.now(), post="user", department=cls.department)
        cls.project = Project.objects.create(name="fds", company=cls.company)
        cls.task = Task.objects.create(date=date.today(), time_worked=120, project=cls.project,
                                       user=cls.test_user, description="afs")

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.task, cls.test_user, cls.project, cls.department, cls.company]:
            elem.delete()

    def test_checking_user_model_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                date_joined=timezone.now(), post="user", department=self.department)

    def test_checking_dunder_str_method_user_model(self):
        self.assertEqual(str(self.test_user), "abc abc")

    def test_checking_username_user_model(self):
        self.assertIsNone(self.test_user.username)

    def test_checking_default_block_user_model(self):
        self.assertEqual(self.test_user.block, False)

    def test_checking_dunder_str_method_company_model(self):
        self.assertEqual(str(self.company), "Abc")

    def test_checking_dunder_str_method_project_model(self):
        self.assertEqual(str(self.project), "fds")

    def test_checking_dunder_str_method_department_model(self):
        self.assertEqual(str(self.department), "abc")
