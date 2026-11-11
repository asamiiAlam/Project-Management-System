from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Chatbox





@receiver(post_save, sender=Project)
def create_project_chatbox(sender, instance, created, **kwargs):
    if created:
        Chatbox.objects.get_or_create(project=instance)