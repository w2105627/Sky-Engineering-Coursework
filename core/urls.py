# Author : w2105627
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.root, name='root'),
    path('teams/', views.teams, name='teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('organisations/', views.organisation, name='organisation'),
    path('departments/', views.departments, name='departments'),
    path('departments/create/', views.create_department, name='create_department'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('teams/<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('teams/<int:team_id>/schedule/', views.schedule_meeting, name='schedule_meeting'),
    path('meetings/<int:meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('meetings/<int:meeting_id>/delete/', views.delete_meeting, name='delete_meeting'),
]
