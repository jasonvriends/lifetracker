from django.contrib import admin
from .models import Diary

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    """Admin configuration for the Diary model."""
    
    list_display = ["user", "title", "entry_date", "created_at", "updated_at"]
    list_filter = ["entry_date", "created_at", "updated_at"]
    search_fields = ["title", "content", "user__email", "user__first_name", "user__last_name"]
    date_hierarchy = "entry_date"
    ordering = ["-entry_date", "-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    
    def get_queryset(self, request):
        """Override to improve performance with select_related."""
        return super().get_queryset(request).select_related("user")
