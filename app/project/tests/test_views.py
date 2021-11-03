from django.test import TestCase
from django.urls import reverse

from user.models import User, Company, Department, Project


def create_companies_and_users():
    company = Company.objects.create(name=f'company')
    for j in range(3):
        Project.objects.create(name=f'project{j}', company=company)
    Department.objects.create(name='department', company=Company.objects.get(id=1))

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


class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/project/list/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/project/index.html')

    def test_list_all_projects(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['projects']), 3)

    def test_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 10}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/project/list/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('project-list', kwargs={'company_id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class EditProjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/project/1/edit/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/project/1/add/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_edit_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-project', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_edit_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_add_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-project', kwargs={'company_id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_post_edit_project(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('edit-project', kwargs={'company_id': 1, 'id': 1}), data={
            'name': 'project0_edited',
            'company': Company.objects.get(id=1)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_post_add_department(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('add-project', kwargs={'company_id': 1}), data={
            'name': 'new_project',
            'project': Company.objects.get(id=1)
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_edit_invalid_project_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 1, 'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 20, 'id': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_add_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-project', kwargs={'company_id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_redirect_not_logged_in(self):
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/project/1/edit/1/')

    def test_add_redirect_not_logged_in(self):
        resp = self.client.get(reverse('add-project', kwargs={'company_id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/project/1/add/')

    def test_edit_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('edit-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')

    def test_add_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('add-project', kwargs={'company_id': 20}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class DeleteDepartmentViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/project/1/delete/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/project/list/1')

    def test_view_url_access_by_name_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/project/list/1')

    def test_deleting_project(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 1, 'id': 2}))
        try:
            project = Project.objects.get(id=2)
        except Project.DoesNotExist:
            project = None
        self.assertEqual(project, None)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/project/list/1')

    def test_invalid_project_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 1, 'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 20, 'id': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/project/1/delete/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('delete-project', kwargs={'company_id': 1, 'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')