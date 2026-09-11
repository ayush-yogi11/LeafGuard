from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm, EmailAuthenticationForm
from .models import CustomUser


class RegisterView(CreateView):
    """Class-based view for registration — auto-logs in the user on success."""
    model = CustomUser
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Your account has been created.")
        return response


class EmailLoginView(LoginView):
    """Login view using the email-based auth form."""
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("core:home")


@login_required
def profile_view(request):
    """
    Shows account tier, remaining scans today, and recent scan history.
    Scan history query itself lives in Phase 4 once ScanHistory exists.
    """
    user = request.user
    context = {
        "remaining_scans": user.get_remaining_scans(),
        "is_premium": user.is_premium,
    }
    return render(request, "accounts/profile.html", context)

from django.utils import timezone

@login_required
def upgrade_view(request):
    """
    Demo upgrade flow. In a real deployment this would integrate a
    payment provider (Stripe, Razorpay, etc.) and only flip is_premium
    inside a verified payment webhook handler — never directly from a
    button click like this. Wiring that up is a natural next step once
    you're ready to charge real users.
    """
    if request.method == "POST":
        request.user.is_premium = True
        request.user.premium_since = timezone.now()
        request.user.save(update_fields=["is_premium", "premium_since"])
        messages.success(request, "You're now a Premium member — unlimited scans unlocked.")
        return redirect("accounts:profile")

    return render(request, "accounts/upgrade.html")