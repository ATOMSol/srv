# admin.py
from django.contrib import admin
from .models import Appointment, AdditionalVisitor
from django.utils.translation import gettext_lazy as _  # For translatable fieldset titles
from django.core.exceptions import ValidationError


class ItemInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = AdditionalVisitor
    extra = 1  # Number of empty forms displayed by default
    can_delete = True  # Allow deleting items
    show_change_link = True  # Optional: Add "Edit" links for related items

@admin.register(Appointment)
class VisitorsAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ('visitor_name',"id")

    # def save_model(self, request, obj, form, change):
    #     try:
    #         obj.clean()  # Validate the object
    #     except ValidationError as e:
    #         form.add_error(None, e.message_dict)  # Add validation errors to the form
    #         return
    #     super().save_model(request, obj, form, change)
