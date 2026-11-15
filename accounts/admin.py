from django.contrib import admin

from .models import OTP, Profile

# Register your models here.
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    search_fields = ('user__username', 'code')
    list_filter = ('created_at',)
admin.site.register(OTP, OTPAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'updated_at')
    search_fields = ('user__username', 'role')
    list_filter = ('role', 'created_at', 'updated_at')
  
admin.site.register(Profile, ProfileAdmin)  