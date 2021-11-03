from django.urls import path
from department import views

urlpatterns = [
    path('list/<company_id>/', views.department_list, name='department-list'),
    path('<company_id>/edit/<id>/', views.edit_department, name='edit-department'),
    path('<company_id>/add/', views.edit_department, name='add-department'),
    path('<company_id>/delete/<id>/', views.delete_department, name='delete-department'),
]