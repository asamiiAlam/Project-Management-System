from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from .permissions import Dept_Permission, Message_Permission, Project_Permission, Task_Permission, can_access_chat
from .serializers import DepartmentSerializer, ProjectSerializer, TaskSerializer, ChatboxSerializer, MessageSerializer, TaskSubmissionSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Department, Notification, Project, TaskSubmission, Tasks, Chatbox, Messages
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,]
    filterset_fields = ['status',  'project__priority']
    search_fields = ['title', 'description', 'assigned_to__username','project__name']
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
class ALL_Tasks_OF_A_User(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'project__priority']
    search_fields = ['title', 'description', 'assigned_to__username','project__name']

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if self.request.user.id != user_id and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view tasks for this user.")
       
        return Tasks.objects.filter(assigned_to_id=user_id, status__in=['In Progress', 'Not Started','On Hold'])




#Notification views
from rest_framework import status
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
   
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskSubmissionListView(generics.ListCreateAPIView):
    queryset = TaskSubmission.objects.all()
    serializer_class = TaskSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task=serializer.validated_data["task"]
        task_id = task.id
        task = Tasks.objects.get(id=task_id)
        if not self.request.user.tasks.filter(id=task_id).exists():
            raise PermissionDenied("You are not assigned to this task.")    
        else:
            serializer.save(task=task, submitted_by=self.request.user)

class ALL_Projects_OF_A_Manager(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['name', 'description']

    def get_queryset(self):
        user_id = self.request.user.id
        return Project.objects.filter(manager_id=user_id)
class ProjectSubmissionsListView(generics.ListAPIView):
    serializer_class = TaskSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        user = self.request.user

        if not (user.is_superuser or project.manager_id == user.id):
            raise PermissionDenied("You are not the manager of this project.")

        return (
            TaskSubmission.objects
            .filter(task__project=project)
            .select_related('task', 'submitted_by')
        )


# ai projct health view
from .services.ai_health import analyze_project_health
class ProjectHealthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(
            Project,
            id=project_id
        )

        # Only project manager or superuser
        if not (
            request.user.is_superuser
            or project.manager_id == request.user.id
        ):
            raise PermissionDenied(
                "You cannot access this project's health report."
            )

        try:
            result = analyze_project_health(project.id)

        except Exception:
            return Response(
                {"detail": "Unable to generate AI health report."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(result, status=status.HTTP_200_OK)


# message summarizer
from .services.chat_summarizer import summarize_project_chat
class ProjectChatSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        project = get_object_or_404(Project, id=project_id)


        if not can_access_chat(request.user, project):
            raise PermissionDenied("You don't have permission to access this project chat.")

        try:
            result = summarize_project_chat(project.id)
            return Response(result, status=200)

        except Exception as e:
            return Response(
                {"detail": "Unable to generate chat summary.", "error": str(e)},
                status=503
            )