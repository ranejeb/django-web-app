from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from user.models import User, Department, Company, Project, Task
from datetime import date


class ViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.project = Project.objects.create(name="abc", company=cls.company)
        cls.test_user1 = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)
        cls.test_user1.department.project.add(cls.project)
        cls.test_user1.set_password("12345")
        cls.test_user1.save()
        cls.test_user2 = User.objects.create(password="", email="def@mail.ru", role=2, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)
        cls.task1 = Task.objects.create(date=date.today(), time_worked=120, description="abc", project=cls.project,
                                        user=cls.test_user1)
        cls.task2 = Task.objects.create(date=date.today(), time_worked=100, description="def", project=cls.project,
                                        user=cls.test_user2)

    @classmethod
    def tearDownClass(cls):
        cls.test_user1.department.project.clear()
        for elem in [cls.task1, cls.task2, cls.project, cls.test_user1, cls.test_user2, cls.department, cls.company]:
            elem.delete()

    def test_check_access_index_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("user-page"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "user/main/index.html")

    def test_check_context_template_index_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("user-page"))
        today = date.today()
        self.assertEqual(resp.context["today"], today)
        self.assertEqual(resp.context["current_year"], today.year)
        self.assertEqual(resp.context["current_month"], today.month)

    def test_1_check_access_tasks_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("list-tasks", args=[2021, 5, 20]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "user/tasks/index.html")

    def test_2_check_access_tasks_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("list-tasks", args=[2001, 5, 20]))
        self.assertEqual(resp.status_code, 404)

    def test_check_context_template_tasks_view(self):
        self.client.force_login(self.test_user1)
        today = date.today()
        resp = self.client.get(reverse("list-tasks", args=[today.year, today.month, today.day]))
        tasks = resp.context["tasks"]
        self.assertEqual(resp.context["date"], today)
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)

    def test_check_access_change_password_user_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("change-password"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_1_post_request_change_password_user_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("change-password"), data={
            "old_password": "12345",
            "password": "abc",
            "password2": "abc"
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_2_post_request_change_password_user_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("change-password"), data={
            "old_password": "12345",
            "password": "abc",
            "password2": "def"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_check_access_change_data_user_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("change-data"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_post_request_change_data_user_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("change-data"), data={
            "last_name": "vsh",
            "first_name": "vsh"
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("home"))

    def test_1_check_access_create_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("create-task", args=[2021, 5, 20]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_2_check_access_create_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("create-task", args=[2001, 5, 20]))
        self.assertEqual(resp.status_code, 404)

    def test_1_post_request_create_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("create-task", args=[2021, 5, 20]), data={
            "project": [f"{self.project.id}"],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("list-tasks", args=[2021, 5, 20]))

    def test_2_post_request_create_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("create-task", args=[2021, 5, 20]), data={
            "project": [],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_3_post_request_create_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("create-task", args=[2001, 5, 20]), data={
            "project": [f"{self.project.id}"],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 404)

    def test_1_check_access_edit_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("edit-task", args=[self.task1.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_2_check_access_edit_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("edit-task", args=[self.task2.id]))
        self.assertEqual(resp.status_code, 404)

    def test_1_post_request_edit_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("edit-task", args=[self.task1.id]), data={
            "project": [f"{self.project.id}"],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("list-tasks", args=[self.task1.date.year, self.task1.date.month,
                                                               self.task1.date.day]))

    def test_2_post_request_edit_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("edit-task", args=[self.task2.id]), data={
            "project": [f"{self.project.id}"],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 404)

    def test_3_post_request_edit_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.post(reverse("edit-task", args=[self.task1.id]), data={
            "project": [],
            "time_worked": ["140"],
            "description": ["add"],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_1_check_access_delete_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("delete-task", args=[self.task1.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("list-tasks", args=[self.task1.date.year, self.task1.date.month,
                                                               self.task1.date.day]))

    def test_2_check_access_delete_task_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("delete-task", args=[self.task2.id]))
        self.assertEqual(resp.status_code, 404)

    def test_check_access_select_tasks_view(self):
        self.client.force_login(self.test_user1)
        resp = self.client.get(reverse("select-tasks"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "selection_form.html")

    def test_1_post_request_select_tasks_view(self):
        self.client.force_login(self.test_user1)
        today = date.today()
        resp = self.client.post(reverse("select-tasks"), data={
            "start_date": ["31/05/2021"],
            "end_date": [f"{today.day}/{today.month}/{today.year}"],
        })
        tasks = resp.context["tasks"]
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "user/tasks/list_tasks.html")

    def test_2_post_request_select_tasks_view(self):
        self.client.force_login(self.test_user1)
        today = date.today()
        resp = self.client.post(reverse("select-tasks"), data={
            "start_date": [f"{today.day + 1}/{today.month}/{today.year}"],
            "end_date": [f"{today.day}/{today.month}/{today.year}"],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "selection_form.html")

    def test_checks_access_with_different_role_index_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("user-page"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_tasks_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("list-tasks", args=[2021, 5, 20]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_unauthorized_user_change_password_user_view(self):
        resp = self.client.get(reverse("change-password"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login/?next=/user/change-password/")

    def test_checks_access_unauthorized_user_change_data_user_view(self):
        resp = self.client.get(reverse("change-data"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login/?next=/user/change-data/")

    def test_checks_access_with_different_role_create_task_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("create-task", args=[2021, 5, 20]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_edit_task_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("edit-task", args=[self.task1.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_delete_task_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("delete-task", args=[self.task1.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")

    def test_checks_access_with_different_role_select_tasks_view(self):
        self.client.force_login(self.test_user2)
        resp = self.client.get(reverse("select-tasks"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/accounts/login")