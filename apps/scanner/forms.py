"""
Upload form with validation: file type, file size, and basic image integrity check.
"""
from django import forms
from django.conf import settings
from PIL import Image


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            "accept": "image/jpeg,image/png",
            "class": "hidden",  # actual UI is the drag-drop zone in Phase 5; this stays hidden
            "id": "id_image",
        })
    )

    def clean_image(self):
        image = self.cleaned_data["image"]

        # --- Size validation ---
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if image.size > max_bytes:
            raise forms.ValidationError(
                f"Image too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        # --- Extension validation ---
        ext = "." + image.name.rsplit(".", 1)[-1].lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise forms.ValidationError(
                f"Unsupported file type. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
            )

        # --- Integrity check: is this actually a readable image, not a renamed file? ---
        try:
            img = Image.open(image)
            img.verify()
            image.seek(0)  # reset pointer — verify() consumes the file stream
        except Exception:
            raise forms.ValidationError("This file could not be read as a valid image.")

        return image