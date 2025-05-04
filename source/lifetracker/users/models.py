from typing import ClassVar
from zoneinfo import available_timezones
import os
from uuid import uuid4
import logging

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, ImageField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import default_storage

from .managers import UserManager

logger = logging.getLogger(__name__)

def get_avatar_path(instance, filename):
    """Generate a unique path for avatar uploads."""
    # Extract just the filename without path
    filename = os.path.basename(filename)
    
    # Ensure the avatars directory exists
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    os.makedirs(avatar_dir, exist_ok=True)
    logger.debug("Avatar directory: %s", avatar_dir)
    
    # Generate unique filename
    ext = filename.split('.')[-1].lower()  # Convert extension to lowercase
    new_filename = f"{uuid4().hex}.{ext}"
    
    # The path to store in the database (relative to MEDIA_ROOT)
    path = os.path.join('avatars', new_filename)
    logger.debug("Generated avatar path: %s", path)
    
    # The full path on disk
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    logger.debug("Full file path: %s", full_path)
    
    # Ensure the file doesn't already exist
    if os.path.exists(full_path):
        # If it exists, generate a new name
        new_filename = f"{uuid4().hex}.{ext}"
        path = os.path.join('avatars', new_filename)
        logger.debug("File exists, generated new path: %s", path)
    
    return path


class User(AbstractUser):
    """
    Default custom user model for Lifetracker.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = CharField(_("First Name"), max_length=150, blank=False)
    last_name = CharField(_("Last Name"), max_length=150, blank=False)
    email = EmailField(_("Email Address"), unique=True)
    timezone = CharField(
        _("Timezone"),
        max_length=32,
        choices=[(tz, tz) for tz in sorted(available_timezones())],
        default="UTC",
    )
    bio = TextField(_("Bio"), blank=True, help_text=_("Brief description for your profile"))
    avatar = ImageField(
        _("Avatar"),
        upload_to=get_avatar_path,
        blank=True,
        null=True,
        max_length=255,  # Increased max_length for longer file paths
    )
    theme = CharField(
        _("Theme"),
        max_length=32,
        blank=True,
        null=True,
        help_text=_("Custom theme preference (overrides system theme)"),
    )
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    def save(self, *args, **kwargs):
        """Override save to handle avatar file cleanup."""
        if self.pk:  # Only handle existing users
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.avatar and (not self.avatar or old_instance.avatar != self.avatar):
                    # Avatar was changed or removed, delete the old file
                    try:
                        old_path = old_instance.avatar.path
                        if os.path.exists(old_path):
                            logger.debug("Deleting old avatar file: %s", old_path)
                            os.remove(old_path)
                    except Exception as e:
                        logger.error("Error deleting old avatar file: %s", e)
            except User.DoesNotExist:
                pass
        
        # Call the parent save method
        super().save(*args, **kwargs)
        
        # Log avatar details after save
        if self.avatar:
            try:
                logger.debug("Avatar after save:")
                logger.debug("- Name: %s", self.avatar.name)
                logger.debug("- URL: %s", self.avatar.url)
                logger.debug("- Path: %s", self.avatar.path)
                if os.path.exists(self.avatar.path):
                    logger.debug("- Size: %s", os.path.getsize(self.avatar.path))
                else:
                    logger.error("Avatar file does not exist after save: %s", self.avatar.path)
            except Exception as e:
                logger.error("Error checking avatar after save: %s", e)

    @property
    def name(self) -> str:
        """Return the user's full name as a property.
        
        Returns:
            str: User's full name
        """
        return self.get_full_name()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_full_name(self) -> str:
        """Return the user's full name by combining first_name and last_name.
        
        Returns:
            str: User's full name
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email.split('@')[0]

    def get_initials(self) -> str:
        """Return the user's initials based on their name.
        
        Returns:
            str: User's initials (up to 2 characters)
        """
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        elif self.last_name:
            return self.last_name[0].upper()
        return self.email[0].upper()
