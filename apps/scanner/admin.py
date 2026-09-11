from django.contrib import admin
from django.utils.html import format_html

from .models import ScanHistory


@admin.register(ScanHistory)
class ScanHistoryAdmin(admin.ModelAdmin):
    """
    Read-mostly admin view for staff to audit scan activity — e.g.
    spotting disease outbreaks clustering geographically/temporally,
    or investigating a user's support request about a bad prediction.
    """
    list_display = ["user", "disease_name", "confidence", "is_healthy", "created_at", "thumbnail"]
    list_filter = ["is_healthy", "created_at", "raw_label"]
    search_fields = ["user__email", "disease_name", "raw_label"]
    readonly_fields = ["user", "image", "disease_name", "raw_label", "confidence",
                       "is_healthy", "symptoms", "treatment", "created_at", "thumbnail"]
    date_hierarchy = "created_at"

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; border-radius: 4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Preview"

    def has_add_permission(self, request):
        # Scans are only ever created through the app's inference flow,
        # never manually via admin — prevents staff from injecting fake data.
        return False