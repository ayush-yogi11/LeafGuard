"""
Custom User model.

Why a custom user model instead of a Profile-extends-User pattern?
Because we need role/tier fields (is_premium, daily_scan_count) queried
constantly by the rate-limiting logic in Phase 3 — keeping them on the
User row avoids an extra JOIN on every single request that touches
scanning. Django strongly recommends starting any new project with a
custom user model even if you don't need it yet, since swapping later
requires a painful migration.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Extends Django's AbstractUser (keeps built-in permission system,
    groups, is_staff/is_superuser flags) but swaps username -> email
    as the login identifier, and adds freemium/role fields.
    """

    class Role(models.TextChoices):
        GUEST = "guest", "Guest"          # not persisted normally; placeholder for anonymous logic
        USER = "user", "Registered User"
        ADMIN = "admin", "Admin / Staff"

    # --- Identity ---
    username = None  # disable the default username field entirely
    email = models.EmailField("email address", unique=True)

    # --- Role & Tier ---
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.USER,
        help_text="Coarse-grained role, distinct from Django's is_staff/is_superuser."
    )
    is_premium = models.BooleanField(
        default=False,
        help_text="Premium users bypass the daily scan rate limit."
    )
    premium_since = models.DateTimeField(null=True, blank=True)

    # --- Freemium scan tracking (used by Phase 3 rate limiter) ---
    daily_scan_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of scans used today. Reset to 0 whenever last_scan_date != today."
    )
    last_scan_date = models.DateField(
        null=True, blank=True,
        help_text="Date of the most recent scan. Used to detect day rollover."
    )

    # --- Profile extras ---
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email & password are prompted automatically

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    # --- Business logic kept ON the model (fat models, thin views) ---

    def get_remaining_scans(self) -> int | None:
        """
        Returns remaining scans for today, or None if unlimited (premium).
        This is the single source of truth the UI and rate limiter both call —
        avoids duplicating the "is today a new day?" logic in multiple places.
        """
        if self.is_premium:
            return None  # unlimited

        self._reset_count_if_new_day()
        limit = settings.FREE_DAILY_SCAN_LIMIT
        return max(limit - self.daily_scan_count, 0)

    def can_scan(self) -> bool:
        """True if the user has scans remaining (or is premium)."""
        remaining = self.get_remaining_scans()
        return remaining is None or remaining > 0

    def register_scan(self):
        """
        Increments the daily scan counter. Called AFTER a successful
        inference so failed uploads don't burn a user's quota.
        """
        self._reset_count_if_new_day()
        self.daily_scan_count += 1
        self.last_scan_date = timezone.localdate()
        self.save(update_fields=["daily_scan_count", "last_scan_date"])

    def _reset_count_if_new_day(self):
        """
        Lazy reset: rather than a cron job resetting every user's counter
        at midnight, we check-and-reset on read. This scales better since
        it's O(1) per active user instead of a scheduled sweep of the
        entire user table.
        """
        today = timezone.localdate()
        if self.last_scan_date != today:
            self.daily_scan_count = 0
            self.last_scan_date = today
            self.save(update_fields=["daily_scan_count", "last_scan_date"])