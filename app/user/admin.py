from django.contrib import admin
from .models import Company, Department, Project, User

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(User)
