from django.urls import path
from project import views

urlpatterns = [
    path('list/<company_id>/', views.project_list, name='project-list'),
    path('<company_id>/edit/<id>/', views.edit_project, name='edit-project'),
    path('<company_id>/add/', views.edit_project, name='add-project'),
    path('<company_id>/delete/<id>/', views.delete_project, name='delete-project'),
]