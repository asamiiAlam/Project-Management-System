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