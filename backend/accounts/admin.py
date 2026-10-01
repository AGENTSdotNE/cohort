from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AppUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ['email', 'full_name', 'email_verified', 'is_staff']
    list_filter = ['email_verified', 'is_staff', 'is_superuser']
    search_fields = ['email', 'full_name']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Profile', {'fields': ['full_name', 'avatar', 'email_verified']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
    ]
    add_fieldsets = [(None, {'fields': ['email', 'full_name', 'password1', 'password2']})]
