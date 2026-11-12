from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone
class OTP(models.Model):
   
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user_otp")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)    

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300  # 5 minutes

    def __str__(self):
        return f"OTP for {self.user.username} - {self.code}"


class Profile(models.Model):

    roles=[
        ('Employee','Employee'),
        ('Manager','Manager'),
    ]
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=roles,
        default='Employee',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Profile for {self.user.username} - {self.role}"

