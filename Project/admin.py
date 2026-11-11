from django.contrib import admin

# Register your models here.
from .models import Chatbox, Department, Messages,Project, Tasks
admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Tasks)
admin.site.register(Chatbox)
admin.site.register(Messages)   