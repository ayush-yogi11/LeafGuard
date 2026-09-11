"""
Tests for the ML service singleton and ScanHistory persistence.
Requires ml_models/plant_disease_model.pth and class_indices.json
to be present, since these exercise real inference — not mocks.
"""
from pathlib import Path

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

from apps.accounts.models import CustomUser
from .ml_service import ModelService
from .models import ScanHistory


def _generate_dummy_leaf_image() -> bytes:
    """Creates an in-memory fake image so tests don't depend on a real file on disk."""
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


class ModelServiceTests(TestCase):
    def test_singleton_returns_same_instance(self):
        service_a = ModelService.get_instance()
        service_b = ModelService.get_instance()
        self.assertIs(service_a, service_b)

    def test_predict_returns_expected_keys(self):
        service = ModelService.get_instance()
        image_bytes = _generate_dummy_leaf_image()
        result = service.predict(io.BytesIO(image_bytes))

        self.assertIn("disease_name", result)
        self.assertIn("confidence", result)
        self.assertIn("raw_label", result)
        self.assertIn("is_healthy", result)
        self.assertTrue(0 <= result["confidence"] <= 100)

    def test_all_38_classes_are_mapped(self):
        service = ModelService.get_instance()
        self.assertEqual(len(service.idx_to_class), 38)


class ScanHistoryModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="scanner@example.com", password="testpass123"
        )

    def test_scan_history_creation(self):
        image = SimpleUploadedFile(
            "leaf.jpg", _generate_dummy_leaf_image(), content_type="image/jpeg"
        )
        scan = ScanHistory.objects.create(
            user=self.user,
            image=image,
            disease_name="Tomato - Late Blight",
            raw_label="Tomato___Late_blight",
            confidence=94.5,
            is_healthy=False,
            symptoms="Test symptoms",
            treatment="Test treatment",
        )
        self.assertEqual(ScanHistory.objects.count(), 1)
        self.assertEqual(scan.user, self.user)
        self.assertIn(str(scan.confidence), str(scan))  # __str__ includes confidence