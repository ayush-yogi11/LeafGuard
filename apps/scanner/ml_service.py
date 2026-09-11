"""
ML Service Layer — Singleton pattern for model loading + inference.

Matches the exact training setup from the notebook:
- Architecture: torchvision resnet18, fc layer replaced for 38 classes.
- Checkpoint format: a dict with keys "model_state_dict", "num_classes",
  "class_to_idx", "id_to_class" — NOT a raw state_dict, NOT a full model.
- class_indices.json contains class_to_idx (name -> index), so we invert
  it here to look up disease names after argmax().
"""
import json
import logging
import threading

import torch
import torch.nn as nn
from torchvision import transforms, models
from django.conf import settings
from PIL import Image

logger = logging.getLogger(__name__)


class ModelLoadError(Exception):
    pass


class InferenceError(Exception):
    pass


class ModelService:
    """
    Thread-safe singleton wrapping the trained ResNet-18 model.

    Usage:
        service = ModelService.get_instance()
        result = service.predict(uploaded_image_file)
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ModelService._instance is not None:
            raise RuntimeError("Use ModelService.get_instance() instead of direct instantiation.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.idx_to_class = {}   # index -> class name (inverted from class_indices.json)
        self.image_size = settings.ML_IMAGE_SIZE

        self._load_model()       # loads model AND builds idx_to_class from checkpoint
        self._build_transform()

        logger.info(f"ModelService running on device: {self.device}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def _load_model(self):
        model_path = settings.ML_MODEL_PATH
        if not model_path.exists():
            raise ModelLoadError(f"Model file not found at {model_path}")

        try:
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)

            # The notebook saves a plain dict wrapper, not a raw state_dict
            # and not a full nn.Module. Pull out what we need from it.
            if not isinstance(checkpoint, dict) or "model_state_dict" not in checkpoint:
                raise ModelLoadError(
                    "Unexpected checkpoint format — expected a dict with a "
                    "'model_state_dict' key, as saved by the training notebook."
                )

            num_classes = checkpoint["num_classes"]

            # Prefer id_to_class embedded directly in the checkpoint (most
            # reliable, since it's guaranteed to match this exact model).
            # Fall back to class_indices.json only if it's missing.
            if "id_to_class" in checkpoint:
                # JSON round-trip in the notebook produces string keys after
                # a real json dump/load, but here it's still a live Python
                # dict with int keys straight from training — normalize to
                # int just in case.
                self.idx_to_class = {int(k): v for k, v in checkpoint["id_to_class"].items()}
            else:
                self._load_class_indices_from_json()

            # Rebuild the EXACT architecture used in training: resnet18
            # with its final fc layer swapped for our number of classes.
            # weights=None here because we're about to overwrite every
            # weight with our trained checkpoint anyway — downloading the
            # pretrained ImageNet weights first would be wasted bandwidth.
            self.model = models.resnet18(weights=None)
            self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
            self.model.load_state_dict(checkpoint["model_state_dict"])

            self.model.to(self.device)
            self.model.eval()  # CRITICAL: disables dropout/batchnorm training behavior

            logger.info(f"Loaded ResNet-18 model with {num_classes} classes.")

        except ModelLoadError:
            raise
        except Exception as e:
            raise ModelLoadError(f"Error loading model: {e}") from e

    def _load_class_indices_from_json(self):
        """
        Fallback path: reads class_indices.json, which the notebook saves
        as class_to_idx (name -> index). We invert it here since inference
        needs index -> name after argmax().
        """
        path = settings.ML_CLASS_INDEX_PATH
        if not path.exists():
            raise ModelLoadError(f"Class index file not found at {path}")

        with open(path, "r") as f:
            class_to_idx = json.load(f)  # {"Apple___Apple_scab": 0, ...}

        self.idx_to_class = {int(v): k for k, v in class_to_idx.items()}

    def _build_transform(self):
        """
        Must exactly match the notebook's eval_transform — using the
        train_transform (with random flips/rotation) here would corrupt
        inference results with unnecessary randomness.
        """
        self.transform = transforms.Compose([
            transforms.Resize((self.image_size, self.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------

    def _preprocess(self, image_file) -> torch.Tensor:
        try:
            img = Image.open(image_file).convert("RGB")
            tensor = self.transform(img)
            tensor = tensor.unsqueeze(0)  # add batch dimension: (1, C, H, W)
            return tensor.to(self.device)
        except Exception as e:
            raise InferenceError(f"Failed to preprocess image: {e}") from e

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def predict(self, image_file) -> dict:
        if self.model is None:
            raise ModelLoadError("Model is not loaded. Check server logs.")

        tensor = self._preprocess(image_file)

        try:
            with torch.no_grad():  # no gradient tracking needed at inference
                outputs = self.model(tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_index = torch.max(probabilities, dim=1)
        except Exception as e:
            raise InferenceError(f"Model inference failed: {e}") from e

        predicted_index = int(predicted_index.item())
        confidence_pct = float(confidence.item()) * 100

        raw_label = self.idx_to_class.get(predicted_index, "Unknown")
        display_name = self._format_label(raw_label)

        return {
            "disease_name": display_name,
            "confidence": round(confidence_pct, 2),
            "raw_label": raw_label,
            "is_healthy": "healthy" in raw_label.lower(),
        }

    @staticmethod
    def _format_label(raw_label: str) -> str:
        cleaned = raw_label.replace("___", " - ").replace("_", " ")
        return cleaned.strip()