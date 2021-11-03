from django.urls import path
from administrator import views

urlpatterns = [
    path('user/<id>/', views.change_user, name='user'),
    path('delete-user/<id>/', views.delete_user, name='delete-user'),
    path('invitation/', views.invite_user, name='invitation'),
    path('', views.index, name='administrator-page'),
]