from django.contrib.auth.admin import UserAdmin
from users.models import User, UserProfile
from django.contrib import admin

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    fieldsets = UserAdmin.fieldsets + (
        (("Custom fields"), {"fields": ("user_type",)}),
    )

admin.site.register(User, CustomUserAdmin)