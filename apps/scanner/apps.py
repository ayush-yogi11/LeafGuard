"""
Loads the ML model into memory exactly once, when the Django app
registry is fully populated (ready()). This runs once per worker
process — under gunicorn with N workers, the model is loaded N times
total (once per process), never once per request.
"""
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class ScannerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scanner"
    verbose_name = "Plant Scanner"

    def ready(self):
        # Import locally (not at module level) to avoid circular imports
        # and to avoid loading TensorFlow/Torch during migrations,
        # collectstatic, or other management commands that don't need it.
        from .ml_service import ModelService

        try:
            ModelService.get_instance()
            logger.info("✅ ML model loaded successfully at startup.")
        except Exception as e:
            # Don't crash the whole app if the model file is temporarily
            # missing (e.g., during initial deploy before model upload) —
            # log loudly instead. Views will surface a friendly error.
            logger.error(f"❌ Failed to load ML model at startup: {e}")