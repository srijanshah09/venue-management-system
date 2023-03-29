from django.contrib import admin
from .models import User, Otp
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'name',
            'mobile',
            'email',
            'profile_image',
            'role',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'name', 'is_staff')
    search_fields = ('username', 'name', 'id', 'email')

admin.site.register(User, UserCustomAdmin)
admin.site.register(Otp)