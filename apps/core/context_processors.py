# apps/core/context_processors.py
"""
Injects site-wide variables into every template's context automatically,
so we don't have to manually pass things like the site name or brand
colors into every single view's context dict.
"""
from django.conf import settings


def site_context(request):
    """
    Available in ALL templates as {{ site_name }}, {{ free_scan_limit }}, etc.
    """
    return {
        "site_name": "Plant Doctor",
        "free_scan_limit": getattr(settings, "FREE_DAILY_SCAN_LIMIT", 3),
    }