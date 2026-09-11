"""
Rate-limiting decorator for the scan view.

Decorator (not middleware) is the right choice here: it applies precisely
to the one view that consumes quota, rather than adding overhead/complexity
to every request through a middleware that would need its own path-matching
logic to know which views to guard.
"""
from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def rate_limit_scan(view_func):
    """
    Blocks the scan view if a free-tier user has exhausted today's quota.
    Must be stacked UNDER @login_required (applied first) since it needs
    request.user to be authenticated.

    Usage:
        @login_required
        @rate_limit_scan
        def scan_view(request):
            ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.can_scan():
            remaining = user.get_remaining_scans()
            messages.error(
                request,
                "You've used all 3 free scans today. Upgrade to Premium for unlimited scans, "
                "or come back tomorrow."
            )
            return redirect("accounts:profile")

        return view_func(request, *args, **kwargs)

    return _wrapped_view