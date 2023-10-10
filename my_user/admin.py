from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from . import models


class UserProfileInline(admin.TabularInline):
    model = models.UserProfile
    extra = 1


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('id', 'username')
    inlines = [UserProfileInline]


class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(models.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'chief_department', 'is_chief')
    list_display_links = ('id', 'user')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
