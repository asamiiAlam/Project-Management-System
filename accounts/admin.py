from django.contrib import admin

from .models import OTP, Profile

# Register your models here.
admin.site.register(OTP)
admin.site.register(Profile)