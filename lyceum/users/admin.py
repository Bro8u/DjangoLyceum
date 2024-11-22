from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile


__all__ = ["UserAdmin", "ProfileInlined"]


class ProfileInlined(admin.TabularInline):
    model = Profile
    can_delete = False
    readonly_fields = ("coffee_count",)


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInlined,)
    readonly_fields = ("date_joined", "last_login")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
