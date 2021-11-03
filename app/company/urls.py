from django.urls import path
from company import views

urlpatterns = [
    path('list/', views.company_list, name='company-list'),
    path('edit/<id>/', views.edit_company, name='edit-company'),
    path('add/', views.edit_company, name='add-company'),
    path('delete/<id>/', views.delete_company, name='delete-company'),
]