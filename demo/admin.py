from django.contrib import admin
from .models import CallNotification, Snacks, SnacksItem, Order,ScreenActivity

# Format CallNotification display
@admin.register(CallNotification)
class CallNotificationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "read")
    list_filter = ("read", "timestamp")
    search_fields = ("sender__username", "receiver__username")
    ordering = ("-timestamp",)

# Format Snacks category
@admin.register(Snacks)
class SnacksAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Format SnacksItem display
@admin.register(SnacksItem)
class SnacksItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "image_preview")
    list_filter = ("category",)
    search_fields = ("name", "category__name")

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

# Format Order display
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("created_by__username",)
    ordering = ("-created_at",)



@admin.register(ScreenActivity)
class ScreenActivityAdmin(admin.ModelAdmin):
    list_display = ('screen_id', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('screen_id',)
    fieldsets = (
        (None, {'fields': ('screen_id', 'is_active')}),
    )
    readonly_fields = ('created_at', 'updated_at')

# admin.site.register(ScreenActivity, ScreenActivityAdmin)
#     )

# admin.site.register(ScreenActivity, ScreenActivityAdmin)