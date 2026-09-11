"""
Tests for CustomUser tier/rate-limit logic — the core freemium business rules.
"""
from django.test import TestCase
from django.utils import timezone
from django.conf import settings

from .models import CustomUser


class CustomUserTierTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="freeuser@example.com", password="testpass123"
        )

    def test_free_user_starts_with_full_quota(self):
        self.assertEqual(self.user.get_remaining_scans(), settings.FREE_DAILY_SCAN_LIMIT)
        self.assertTrue(self.user.can_scan())

    def test_quota_decrements_on_scan(self):
        self.user.register_scan()
        self.assertEqual(self.user.daily_scan_count, 1)
        self.assertEqual(
            self.user.get_remaining_scans(), settings.FREE_DAILY_SCAN_LIMIT - 1
        )

    def test_free_user_blocked_after_limit(self):
        for _ in range(settings.FREE_DAILY_SCAN_LIMIT):
            self.user.register_scan()
        self.assertFalse(self.user.can_scan())
        self.assertEqual(self.user.get_remaining_scans(), 0)

    def test_quota_resets_on_new_day(self):
        for _ in range(settings.FREE_DAILY_SCAN_LIMIT):
            self.user.register_scan()
        self.assertFalse(self.user.can_scan())

        # Simulate yesterday's last scan
        self.user.last_scan_date = timezone.localdate() - timezone.timedelta(days=1)
        self.user.save()

        self.assertTrue(self.user.can_scan())
        self.assertEqual(self.user.daily_scan_count, 0)

    def test_premium_user_has_unlimited_scans(self):
        self.user.is_premium = True
        self.user.save()
        for _ in range(settings.FREE_DAILY_SCAN_LIMIT + 5):
            self.user.register_scan()
        self.assertIsNone(self.user.get_remaining_scans())
        self.assertTrue(self.user.can_scan())

    def test_email_is_the_username_field(self):
        self.assertEqual(CustomUser.USERNAME_FIELD, "email")
        self.assertTrue(self.user.check_password("testpass123"))