
from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('departments/<int:department_id>/projects/', views.DepartmentProjectsListView.as_view(), name='department-projects-list'),
    path('chatboxes/admins/', views.Chatboxes_For_Admins.as_view(), name='chatboxes-for-admins'),
    path('chatboxes/admins/<int:pk>/', views.ChatboxDetailView_FOR_Admins.as_view(), name='chatbox-detail'),
    path('chatboxes/<int:project_id>/', views.ChatboxListView.as_view(), name='chatbox-detail'),
    
    path('messages/', views.MessegaseListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    
]