from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import UserManager


class Company(models.Model):
    """Модель, описывающая таблицу Company"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Модель, описывающая таблицу Project"""
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Department(models.Model):
    """Модель, описывающая таблицу Department"""
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    project = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Модель, описывающая таблицу User"""
    username = None
    email = models.EmailField(unique=True)
    role = models.SmallIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, null=True)
    post = models.CharField(max_length=200)
    block = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Task(models.Model):
    """Модель, описывающая таблицу Task"""
    date = models.DateField()
    time_worked = models.PositiveBigIntegerField()
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
