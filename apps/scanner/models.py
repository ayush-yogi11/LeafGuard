"""
ScanHistory: logs every leaf scan a user performs, along with the
model's prediction, so users can review past results and staff can
audit usage patterns.
"""
from django.conf import settings
from django.db import models


def scan_image_upload_path(instance, filename):
    """
    Organizes uploaded scan images by date: media/scans/2026/08/31/filename.jpg
    Keeps the media folder from becoming one giant flat directory as
    usage grows, and makes it easy to archive/clean up by date later.
    """
    from django.utils import timezone
    now = timezone.now()
    return f"scans/{now.year}/{now.month:02d}/{now.day:02d}/{filename}"


class ScanHistory(models.Model):
    """One row per leaf image a user has submitted for diagnosis."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scans",
        help_text="The user who submitted this scan.",
    )
    image = models.ImageField(
        upload_to=scan_image_upload_path,
        help_text="The uploaded leaf photo.",
    )

    # --- Prediction results (denormalized/snapshotted at scan time) ---
    disease_name = models.CharField(
        max_length=255,
        help_text="Human-readable disease name at the time of scanning.",
    )
    raw_label = models.CharField(
        max_length=255,
        help_text="Original model class label, e.g. 'Tomato___Late_blight'.",
    )
    confidence = models.FloatField(
        help_text="Model's confidence percentage (0-100) for this prediction.",
    )
    is_healthy = models.BooleanField(default=False)

    # --- Snapshotted knowledge-base content ---
    # We COPY symptoms/treatment text into the row at scan time, rather
    # than looking it up live from disease_data.py each time the result
    # is viewed. This means historical scans stay accurate even if the
    # knowledge base wording is edited later — a user's 3-month-old scan
    # result won't silently change underneath them.
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Scan History"
        verbose_name_plural = "Scan History"
        indexes = [
            # Speeds up the most common query: "this user's scans, newest first"
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.disease_name} ({self.confidence}%)"