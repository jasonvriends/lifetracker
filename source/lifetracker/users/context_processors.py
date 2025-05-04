from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from allauth.mfa.models import Authenticator

User = get_user_model()

def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }

def mfa_context(request):
    """
    Add MFA-related context variables to the context.
    """
    context = {}
    if request.user.is_authenticated:
        # Check if TOTP is enabled for the user
        context['totp_enabled'] = Authenticator.objects.filter(user=request.user, type='totp').exists()
    return context
