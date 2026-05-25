from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('team/<int:team_id>/', views.team_profile, name='team_profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:team_id>/', views.team_profile, name='team_profile'),
    path('teams/<int:team_id>/join/', views.join_team, name='join_team'),
    path('teams/<int:team_id>/leave/', views.leave_team, name='leave_team'),
]