from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from .permissions import Dept_Permission, Message_Permission, Project_Permission, Task_Permission, can_access_chat
from .serializers import DepartmentSerializer, ProjectSerializer, TaskSerializer, ChatboxSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Department, Project, Tasks, Chatbox, Messages
from rest_framework.views import APIView
from rest_framework.response import Response
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


#all projects of a particular department
class DepartmentProjectsListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,Project_Permission]

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        return Project.objects.filter(department_id=department_id)




class ChatboxListView(APIView):

    def get(self, request, project_id):
        try:
            chatbox = Chatbox.objects.get(project_id=project_id)
        except Chatbox.DoesNotExist:
            return Response({"detail": "Chatbox not found."}, status=404)

        if not can_access_chat(request.user, chatbox.project):
            raise PermissionDenied("You do not have permission to access this chatbox.")

        serializer = ChatboxSerializer(chatbox)
        return Response(serializer.data)
    

   
   

class MessegaseListView(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,Message_Permission]
    def perform_create(self, serializer):
        chatbox = serializer.validated_data["chatbox"]
        if not can_access_chat(self.request.user, chatbox.project):
            raise PermissionDenied("You do not have permission to send messages in this chatbox.")
        
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, Message_Permission]


from .permissions import Chatbox_Permission
class Chatboxes_For_Admins(generics.ListCreateAPIView):
    queryset = Chatbox.objects.all()
    serializer_class = ChatboxSerializer
    permission_classes = [IsAuthenticated, Chatbox_Permission]

class ChatboxDetailView_FOR_Admins(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chatbox.objects.all()
    serializer_class = ChatboxSerializer
    permission_classes = [IsAuthenticated, Chatbox_Permission]
    





