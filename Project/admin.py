from django.contrib import admin

# Register your models here.
from .models import Chatbox, Department, Messages, Notification, TaskSubmission ,Project, Tasks
admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Tasks)
admin.site.register(Chatbox)
admin.site.register(Messages)   
admin.site.register(Notification)
admin.site.register(TaskSubmission)