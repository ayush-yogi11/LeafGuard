"""
Scanner views: upload UI, inference trigger, and result display.

Note: ScanHistory persistence is wired in here but the model itself is
defined in Phase 4 — I'm referencing it now so the view is complete and
you can see the full request flow, then Phase 4 gives you the migration.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .decorators import rate_limit_scan
from .forms import ImageUploadForm
from .ml_service import ModelService, ModelLoadError, InferenceError
from .disease_data import get_disease_info
from .models import ScanHistory  # defined in Phase 4

logger = logging.getLogger(__name__)


@login_required
@rate_limit_scan
def scan_view(request):
    """
    GET: renders the drag-and-drop upload UI.
    POST: runs inference, saves ScanHistory, redirects to the result page.
    """
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_file = form.cleaned_data["image"]

            try:
                service = ModelService.get_instance()
                result = service.predict(image_file)
            except (ModelLoadError, InferenceError) as e:
                logger.error(f"Scan failed for user {request.user.email}: {e}")
                messages.error(request, "Sorry, scanning is temporarily unavailable. Please try again shortly.")
                return redirect("scanner:scan")

            disease_info = get_disease_info(result["raw_label"])

            # Persist to history BEFORE incrementing quota, so a DB failure
            # doesn't silently burn the user's scan without a record of it.
            scan = ScanHistory.objects.create(
                user=request.user,
                image=image_file,
                disease_name=result["disease_name"],
                confidence=result["confidence"],
                symptoms=disease_info["symptoms"],
                treatment=disease_info["treatment"],
            )

            # Only count against quota on a genuinely successful scan.
            request.user.register_scan()

            return redirect("scanner:result", pk=scan.pk)

        # form invalid — fall through and re-render with errors
    else:
        form = ImageUploadForm()

    context = {
        "form": form,
        "remaining_scans": request.user.get_remaining_scans(),
    }
    return render(request, "scanner/scan.html", context)


@login_required
def result_view(request, pk):
    """Shows a single scan result. Restricted to the owning user for privacy."""
    scan = ScanHistory.objects.filter(pk=pk, user=request.user).first()
    if scan is None:
        messages.error(request, "Scan not found.")
        return redirect("scanner:scan")

    return render(request, "scanner/result.html", {"scan": scan})


@login_required
def history_view(request):
    """Paginated list of the user's past scans, most recent first."""
    scans = ScanHistory.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "scanner/history.html", {"scans": scans})