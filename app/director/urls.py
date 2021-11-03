from django.urls import path
from director import views

urlpatterns = [
    path('user-data/<int:user_id>', views.user_data, name='user-data'),
    path('users-data-selection/', views.users_data_selection, name='users-data-selection'),
    path('', views.index, name='director-page'),
]
