from django.contrib import admin
from .models import LostItem, FoundItem, ActivityLog, ClaimProcessing, ClaimDone

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "student_name", "location", "priority", "is_resolved", "created_at")
    list_filter = ("priority", "is_resolved")
    search_fields = ("item_name", "student_name", "location")

@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "student_name", "location", "priority", "is_resolved", "created_at")
    list_filter = ("priority", "is_resolved")
    search_fields = ("item_name", "student_name", "location")

@admin.register(ClaimProcessing)
class ClaimProcessingAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "student_name", "location", "priority", "lost_item", "created_at")
    list_filter = ("priority",)
    search_fields = ("item_name", "student_name", "location")

@admin.register(ClaimDone)
class ClaimDoneAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "student_name", "location", "priority", "lost_item", "claimed_at")
    list_filter = ("priority",)
    search_fields = ("item_name", "student_name", "location")

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("id", "action_type", "category", "description", "item_id", "created_at")
