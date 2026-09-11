"""
ALTERNATIVE to the decorator above. Not currently active — apps.scanner
uses the decorator approach in views.py instead. Kept here in case you
later want request-level enforcement across multiple scan-related paths
without decorating each view individually.

To activate: add "apps.scanner.middleware.ScanRateLimitMiddleware" to
MIDDLEWARE in settings/base.py, positioned AFTER AuthenticationMiddleware
(it needs request.user resolved first).
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class ScanRateLimitMiddleware:
    """Blocks POST requests to the scan endpoint once a free user's quota is used up."""

    PROTECTED_PATH_NAME = "scanner:scan"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path == reverse(self.PROTECTED_PATH_NAME):
            if request.user.is_authenticated and not request.user.can_scan():
                messages.error(request, "Daily free scan limit reached. Upgrade to Premium.")
                return redirect("accounts:profile")

        return self.get_response(request)