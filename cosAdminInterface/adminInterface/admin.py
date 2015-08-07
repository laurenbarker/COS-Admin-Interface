from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission

from adminInterface.models import AdminUser

class PermissionAdmin(admin.ModelAdmin):
	search_fields = ['name', 'codename']

admin.site.register(Permission, PermissionAdmin)
