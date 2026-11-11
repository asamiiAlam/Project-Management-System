from django.db import models
from django.conf import settings

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Project(models.Model):
    name = models.CharField(max_length=100)
    status_choices = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Not Started')
    manager=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_projects')
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name
class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    status_choices = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Not Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title



class Chatbox(models.Model):
    project = models.OneToOneField(
        'Project',
        on_delete=models.CASCADE,
        related_name='chatbox'
    )

    def __str__(self):
        return f"Chatbox for {self.project.name}"


class Messages(models.Model):
    chatbox = models.ForeignKey(
        Chatbox,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


