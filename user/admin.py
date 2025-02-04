from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Customize the admin panel for User
class UserAdmin(UserAdmin):
    model = User
    # Add custom fields to the "add user" and "change user" forms in the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('gm','role', 'phone_number'),
        }),
    )
    # Add custom fields to the "create user" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('gm','role', 'phone_number'),
        }),
    )

    # Specify the fields to display in the user list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    # Enable search by custom fields
    search_fields = ('username', 'email', 'role', 'phone_number')

# Register the custom user model with the custom admin class
admin.site.register(User, UserAdmin)
