from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Chatbox, Tasks, Notification

from django.db.models.signals import pre_save


@receiver(post_save, sender=Project)
def create_project_chatbox(sender, instance, created, **kwargs):
    if created:
        Chatbox.objects.get_or_create(project=instance)



@receiver(pre_save, sender=Tasks)
def remember_old_assignee(sender, instance, **kwargs):
    if instance.pk:
        instance._old_assigned_to_id = (
            Tasks.objects.filter(pk=instance.pk)
            .values_list("assigned_to_id", flat=True)
            .first()
        )
    else:
        instance._old_assigned_to_id = None


@receiver(post_save, sender=Tasks)
def notify_task_assignment(sender, instance, created, **kwargs):
    old_id = getattr(instance, "_old_assigned_to_id", None)

    if created or old_id != instance.assigned_to_id:
        Notification.objects.create(
            user=instance.assigned_to,
            task=instance,
            message=f"You have been assigned a new task: {instance.title} "
                    f"(project: {instance.project.name})",
        )