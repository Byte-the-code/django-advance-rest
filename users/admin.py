from django.contrib.auth.admin import UserAdmin
from users.models import User, UserProfile, UserDocumentation
from django.contrib import admin

@admin.register(UserDocumentation)
class UserDocumentationAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'document_identifier', 'status')

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    fieldsets = UserAdmin.fieldsets + (
        (("Custom fields"), {"fields": ("user_type",)}),
    )

admin.site.register(User, CustomUserAdmin)