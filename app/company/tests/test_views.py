from django.test import TestCase
from django.urls import reverse

from user.models import User, Company, Department


def create_companies_and_users():
    for i in range(3):
        Company.objects.create(name=f'company{i}')
    department = Department.objects.create(name='department1', company=Company.objects.get(id=1))

    admin = User.objects.create_user(
        first_name=f'admin',
        last_name=f'admin',
        email=f'admin@email.com',
        department=department,
        post="admin",
        role=1,
        password='12345678'
    )
    not_admin = User.objects.create_user(
        first_name=f'not admin',
        last_name=f'not admin',
        email=f'not_admin@email.com',
        department=department,
        post="not_admin",
        role=3,
        password='12345678'
    )

    return admin, not_admin


class CompanyListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/company/list/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('company-list'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('company-list'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/company/index.html')

    def test_list_all_companies(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('company-list'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['companies']), 3)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('company-list'))
        self.assertRedirects(resp, '/accounts/login/?next=/company/list/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('company-list'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class EditCompanyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_edit_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/company/edit/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/company/add/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_edit_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-company', kwargs={'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_add_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-company'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_edit_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-company', kwargs={'id': 1}))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_add_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('add-company'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'base_form.html')

    def test_post_edit_company(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('edit-company', kwargs={'id': 1}), data={
            'name': 'company1_edited'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/company/list')

    def test_post_add_company(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('add-company', ), data={
            'name': 'new_company'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/company/list')

    def test_edit_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('edit-company', kwargs={'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_redirect_not_logged_in(self):
        resp = self.client.get(reverse('edit-company', kwargs={'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/company/edit/1/')

    def test_add_redirect_not_logged_in(self):
        resp = self.client.get(reverse('add-company'))
        self.assertRedirects(resp, '/accounts/login/?next=/company/add/')

    def test_edit_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('edit-company', kwargs={'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')

    def test_add_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('add-company'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class DeleteCompanyViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.admin, cls.not_admin = create_companies_and_users()

    def test_view_url_exists_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/company/delete/1/')
        self.assertRedirects(resp, reverse('company-list'))

    def test_view_url_access_by_name_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-company', kwargs={'id': 1}))
        self.assertRedirects(resp, reverse('company-list'))

    def test_deleting_company(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-company', kwargs={'id': 2}))
        try:
            company = Company.objects.get(id=2)
        except Company.DoesNotExist:
            company = None
        self.assertEqual(company, None)
        self.assertRedirects(resp, reverse('company-list'))

    def test_invalid_company_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-company', kwargs={'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('delete-company', kwargs={'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/company/delete/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('delete-company', kwargs={'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')
