from django.contrib import admin

# Register your models here.
from .models import Department,Project, Tasks
admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Tasks)