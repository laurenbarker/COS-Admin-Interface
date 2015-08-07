from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission

from adminInterface.models import AdminUser

# class AdminUserInline(admin.StackedInline):
# 	model = AdminUser
# 	can_delete = False

#class UserAdmin(UserAdmin):
   # inlines = (AdminUserInline, )
   # fields = ['user_permissions']
   # exclude = ('first_name', 'last_name',)

class PermissionAdmin(admin.ModelAdmin):
	search_fields = ['name', 'codename']

#admin.site.unregister(User)
a#dmin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)