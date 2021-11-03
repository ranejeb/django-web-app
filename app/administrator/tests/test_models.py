from django.test import TestCase

from administrator.models import UnregisteredUser
from user.models import Company, Department


class UnregisteredUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(name='company1')
        department = Department.objects.create(name='department1', company=company)
        UnregisteredUser.objects.create(
            first_name='John',
            last_name='Connor',
            email='JohnConnor@email.com',
            department=department,
            post="mankind's last hope",
            role=3,
            code='12345678'
            )

    def test_first_name_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_email_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_department_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('department').verbose_name
        self.assertEquals(field_label, 'department')

    def test_post_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'post')

    def test_role_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('role').verbose_name
        self.assertEquals(field_label, 'role')

    def test_code_label(self):
        user = UnregisteredUser.objects.get(id=1)
        field_label = user._meta.get_field('code').verbose_name
        self.assertEquals(field_label, 'code')

    def test_first_name_max_length(self):
        user = UnregisteredUser.objects.get(id=1)
        max_length = user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 150)

    def test_last_name_max_length(self):
        user = UnregisteredUser.objects.get(id=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 150)

    def test_email_max_length(self):
        user = UnregisteredUser.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 254)

    def test_post_max_length(self):
        user = UnregisteredUser.objects.get(id=1)
        max_length = user._meta.get_field('post').max_length
        self.assertEquals(max_length, 200)

    def test_code_max_length(self):
        user = UnregisteredUser.objects.get(id=1)
        max_length = user._meta.get_field('code').max_length
        self.assertEquals(max_length, 8)

    def test_object_name(self):
        user = UnregisteredUser.objects.get(id=1)
        expected_object_name = f'{user.first_name} {user.last_name}'
        self.assertEquals(expected_object_name, str(user))

    def test_generate_code(self):
        user = UnregisteredUser.objects.get(id=1)
        code = user.generate_code()
        self.assertTrue(type(code) == str and len(code) == 8)
