from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department,Project,Tasks

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'created_by', 'title', 'description', 'project', 'assigned_to', 'status', 'start_date', 'finish_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        finish_date = attrs.get(
            "finish_date",
            getattr(self.instance, "finish_date", None)
        )

        if start_date and finish_date and finish_date < start_date:
            raise serializers.ValidationError({
                "finish_date": "Finish date cannot be earlier than start date."
            })
    

        return attrs
    
class ProjectSerializer(serializers.ModelSerializer):
    tasks=TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'department', 'manager', 'status', 'start_date', 'finish_date', 'created_at', 'updated_at', 'tasks']
        read_only_fields = ['id', 'created_at', 'updated_at','manager']
    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        finish_date = attrs.get(
            "finish_date",
            getattr(self.instance, "finish_date", None)
        )

        if start_date and finish_date and finish_date < start_date:
            raise serializers.ValidationError({
                "finish_date": "Finish date cannot be earlier than start date."
            })

        return attrs

