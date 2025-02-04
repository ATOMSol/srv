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
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'roles')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Team info'), {'fields': ('gm',)}),
    )
    
    # List display settings
    list_display = ('phone', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')
    
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
