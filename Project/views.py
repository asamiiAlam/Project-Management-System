from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from .permissions import Dept_Permission, Project_Permission, Task_Permission
from .serializers import DepartmentSerializer, ProjectSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Department, Project, Tasks

# Create your views here.
class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, Dept_Permission]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, Dept_Permission]

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,Project_Permission]
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,Project_Permission]
class TaskListView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,Task_Permission]
    def perform_create(self, serializer):
      
        project = serializer.validated_data["project"]

        if (
        not self.request.user.is_superuser
        and project.manager_id != self.request.user.id
        ):
          raise PermissionDenied(
            "You are not the manager of this project."
          )

        serializer.save(created_by=self.request.user)
    
       
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,Task_Permission]


