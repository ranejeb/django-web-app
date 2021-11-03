from django.test import TestCase
from django.urls import reverse

from user.models import User, Company, Department


def create_company_and_users():
    company = Company.objects.create(name='company1')
    department = Department.objects.create(name='department1', company=company)

    User.objects.create_user(
        first_name='John',
        last_name='Connor',
        email='JohnConnor@email.com',
        department=department,
        post="mankind's last hope",
        role=3,
        password='12345678'
    )

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

    return company, department, admin, not_admin


class AdminIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company, department, cls.admin, cls.not_admin = create_company_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/administrator/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('administrator-page'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('administrator-page'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/index.html')

    def test_list_all_users(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('administrator-page'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['users']), 3)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('administrator-page'))
        self.assertRedirects(resp, '/accounts/login/?next=/administrator/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('administrator-page'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class ChangeUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company, cls.department, cls.admin, cls.not_admin = create_company_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/administrator/user/1/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_post_request_change_user(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('user', kwargs={'id': 1}), data={
            'department': self.department,
            'is_active': True
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/change-user.html')

    def test_invalid_user_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('user', kwargs={'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('user', kwargs={'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/administrator/user/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('user', kwargs={'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class DeleteUserViewTest(TestCase):
    @classmethod
    def setUp(cls):
        company, cls.department, cls.admin, cls.not_admin = create_company_and_users()

    def test_view_url_exists_and_redirect(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/administrator/delete-user/1/')
        self.assertRedirects(resp, reverse('administrator-page'))

    def test_deleting_user(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-user', kwargs={'id': 1}))
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            user = None
        self.assertEqual(user, None)
        self.assertRedirects(resp, reverse('administrator-page'))

    def test_invalid_user_id(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-user', kwargs={'id': 20}))
        self.assertEqual(resp.status_code, 404)

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('delete-user', kwargs={'id': 1}))
        self.assertRedirects(resp, '/accounts/login/?next=/administrator/delete-user/1/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('delete-user', kwargs={'id': 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')


class InviteUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company, cls.department, cls.admin, cls.not_admin = create_company_and_users()

    def test_view_url_exists(self):
        self.client.force_login(self.admin)
        resp = self.client.get('/administrator/invitation/')
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('invitation'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)

    def test_use_correct_template(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('invitation'))
        self.assertEqual(str(resp.context['user']), 'admin admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/invitation.html')

    def test_post_request_change_user(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('invitation'), data={
            'first_name': 'Sara',
            'last_name': 'Connor',
            'email': 'saraconnor@email.com',
            'department': self.department,
            'post': 'waitress',
            'role': 3
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'administrator/invitation.html')

    def test_redirect_not_logged_in(self):
        resp = self.client.get(reverse('invitation'))
        self.assertRedirects(resp, '/accounts/login/?next=/administrator/invitation/')

    def test_redirect_not_admin(self):
        self.client.force_login(self.not_admin)
        resp = self.client.get(reverse('invitation'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login')
