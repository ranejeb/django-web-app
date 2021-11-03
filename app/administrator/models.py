from string import ascii_letters, digits
from secrets import choice
from django.db import models
from user.models import Department


class UnregisteredUser(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    post = models.CharField(max_length=200)
    role = models.SmallIntegerField(default=3)
    code = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def generate_code(self):
        letters_and_digits = ascii_letters + digits
        code = ''.join(choice(letters_and_digits) for i in range(8))
        return code
