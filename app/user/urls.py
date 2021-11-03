from django.urls import path
from user import views

urlpatterns = [
    path('list-tasks/<int:year>/<int:month>/<int:day>/', views.tasks, name='list-tasks'),
    path('create-task/<int:year>/<int:month>/<int:day>/', views.create_task, name='create-task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit-task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete-task'),
    path('select-tasks/', views.select_tasks, name='select-tasks'),
    path('change-data/', views.change_data_user, name='change-data'),
    path('change-password/', views.change_password_user, name='change-password'),
    path('', views.index, name='user-page'),
]
