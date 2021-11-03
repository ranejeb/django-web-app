from django.test import TestCase
from django.urls import reverse

from user.models import User, Company, Department, Project


def create_companies_and_users():
    for i in range(3):
        company = Company.objects.create(name=f'company{i}')
        for j in range(3):
            Department.objects.create(name=f'department{i*j}', company=company)

    admin = User.objects.create_user(
        first_name=f'admin',
        last_name=f'admin',
        email=f'admin@email.com',
        department=Department.objects.get(id=1),
        post="admin",
        role=1,
        password='12345678'
    )
    not_admin = User.objects.create_user(
        first_name=f'not admin',
        last_name=f'not admin',
        email=f'not_admin@email.com',
        department=Department.objects.get(id=1),
        post="not_admin",
        role=3,
        password='12345678'
    )

    return admin, not_admin


class DepartmentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/department/list/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/department/index.html')

    def test_list_all_departments(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['departments']), 3)

    def test_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 10}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/department/list/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('department-list', kwargs={'company_id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class EditDepartmentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()
        cls.project1 = Project.objects.create(name='project1', company=Company.objects.get(id=1))
        cls.project2 = Project.objects.create(name='project2', company=Company.objects.get(id=1))

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/department/1/edit/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/department/1/add/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_edit_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-department', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_edit_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_add_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-department', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_post_edit_department(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('edit-department', kwargs={'company_id': 1, 'id': 1}), data={
            'name': 'department1_edited',
            'project': [self.project1, self.project2]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_post_add_department(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('add-department', kwargs={'company_id': 1}), data={
            'name': 'department1_edited',
            'project': [self.project1, self.project2]
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_edit_invalid_department_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 1, 'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 20, 'id': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_add_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-department', kwargs={'company_id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_redirect_not_logged_in(self):
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/department/1/edit/1/')

    def test_add_redirect_not_logged_in(self):
        resp = self.client.get(reverse('add-department', kwargs={'company_id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/department/1/add/')

    def test_edit_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('edit-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')

    def test_add_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('add-department', kwargs={'company_id': 20}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class DeleteDepartmentViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/department/1/delete/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/department/list/1')

    def test_view_url_access_by_name_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/department/list/1')

    def test_deleting_department(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 1, 'id': 2}))
        try:
            department = Department.objects.get(id=2)
        except Department.DoesNotExist:
            department = None
        self.assertEqual(department, None)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/department/list/1')

    def test_invalid_department_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 1, 'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 20, 'id': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/department/1/delete/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('delete-department', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')