from typing import ClassVar
from zoneinfo import available_timezones

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Lifetracker.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = CharField(_("First Name"), max_length=150, default="")
    last_name = CharField(_("Last Name"), max_length=150, default="")
    email = EmailField(_("Email Address"), unique=True)
    timezone = CharField(
        _("Timezone"),
        max_length=50,
        default="UTC",
        choices=[(tz, tz) for tz in sorted(available_timezones())],
        help_text=_("Your local timezone for accurate time display"),
    )
    bio = TextField(_("Bio"), blank=True, help_text=_("Brief description for your profile"))
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_initials(self) -> str:
        """Return the user's initials."""
        return f"{self.first_name[0]}{self.last_name[0]}".upper() if self.first_name and self.last_name else self.email[0].upper()
