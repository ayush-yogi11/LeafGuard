from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser

# Shared styling applied to form fields across both auth forms.
INPUT_CLASSES = (
    "w-full px-4 py-2.5 border border-gray-300 rounded-lg "
    "focus:ring-2 focus:ring-[#4E9F3D] focus:border-[#4E9F3D] focus:outline-none"
)


class RegisterForm(UserCreationForm):
    """Registration form using email instead of username."""

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": INPUT_CLASSES,
        "placeholder": "you@example.com",
    }))

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASSES)

        # These labels/help_text tweaks belong ONLY here — this form is the
        # only one with password1/password2 fields. EmailAuthenticationForm
        # below has a single "password" field and must never reference these.
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = None
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = None


class EmailAuthenticationForm(AuthenticationForm):
    """
    Login form — relabels 'username' to work as an email field, and
    explicitly styles the inherited password field. Deliberately does NOT
    touch password1/password2 — this form has no such fields.
    """

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": INPUT_CLASSES,
        "placeholder": "you@example.com",
        "autofocus": True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": INPUT_CLASSES,
        "placeholder": "••••••••",
    }))