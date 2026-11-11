from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_manager(user):
    return user.is_authenticated and (
        user.is_superuser or getattr(getattr(user, 'profile', None), 'role', None) == 'Manager'
    )

class Dept_Permission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser
      
    def has_object_permission(self, request, view, obj):
        return  request.user.is_staff or request.user.is_superuser

class Project_Permission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_manager(request.user) or request.user.is_superuser
      
    def has_object_permission(self, request, view, obj):
        return  request.user.is_superuser or obj.manager == request.user

class Task_Permission(BasePermission):
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True
        return is_manager(request.user) or request.user.is_superuser
      
    def has_object_permission(self, request, view, obj):
        return  request.user.is_superuser or obj.created_by == request.user

#permissions of the chatbox and messages
def is_project_member(user, project):
    return project.tasks.filter(assigned_to=user).exists()


def can_access_chat(user, project):
    return user.is_authenticated and (
        user.is_superuser
        or project.manager_id == user.id
        or is_project_member(user, project)
    )

class Chatbox_Permission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_manager(request.user) or request.user.is_superuser
      
    def has_object_permission(self, request, view, obj):
        return  request.user.is_superuser or request.user.is_staff

class Message_Permission(BasePermission):
    

    def has_object_permission(self, request, view, obj):
        return can_access_chat(request.user, obj.chatbox.project)
        

