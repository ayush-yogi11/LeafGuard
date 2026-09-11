from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Extends Django's built-in UserAdmin so we keep the polished
    permissions/groups widgets, but repoints fieldsets at our
    email-based model and surfaces the freemium fields for support staff.
    """
    ordering = ["-date_joined"]
    list_display = ["email", "role", "is_premium", "daily_scan_count", "is_staff", "is_active"]
    list_filter = ["role", "is_premium", "is_staff", "is_active"]
    search_fields = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar", "bio")}),
        ("Role & Tier", {"fields": ("role", "is_premium", "premium_since")}),
        ("Scan Quota", {"fields": ("daily_scan_count", "last_scan_date")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )