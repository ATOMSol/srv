from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role
from django.utils.translation import gettext_lazy as _

# Register the Role model in the admin
admin.site.register(Role)

# CustomUser Admin Configuration
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define the fieldsets for the admin form layout
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'pass_key')}),
        (("Group"), {"fields": ("groups","user_permissions")}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'roles')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Team info'), {'fields': ('gm',)}),
    )
    
    # List display settings
    list_display = ('phone','unique_id', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
    
    # Search fields
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    
    # Add filter for roles
    list_filter = ('is_staff', 'is_active', 'roles')

    # Define what fields are required for creating a user
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2','pass_key')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Update ordering to use 'phone' instead of 'username'
    ordering = ('phone',)

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)





















from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class UserInline(admin.TabularInline):
    model = User.groups.through  # This is the intermediate model for the ManyToManyField
    extra = 0
    verbose_name = "User"
    verbose_name_plural = "Users"

class GroupAdmin(BaseGroupAdmin):
    inlines = [UserInline]

# Unregister the default Group admin and register your customized one
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
