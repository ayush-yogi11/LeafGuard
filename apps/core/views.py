"""
Landing/home page and simple static pages (about, contact).
Kept intentionally simple — the scanning and blog functionality live
in their own apps; this app is just the site's public-facing shell.
"""
from django.shortcuts import render


def home_view(request):
    """Public landing page. Shown to both guests and logged-in users."""
    return render(request, "core/home.html")