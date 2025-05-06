from django.db import models
from django.conf import settings
from django.utils import timezone
import pytz

class Diary(models.Model):
    """Diary entry model for recording daily journal entries."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_entries"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entry_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "Diary Entries"
        ordering = ["-entry_date", "-created_at"]
        # Ensure users can have only one entry per date
        constraints = [
            models.UniqueConstraint(
                fields=["user", "entry_date"],
                name="unique_diary_entry_per_day"
            )
        ]
    
    def __str__(self):
        """String representation of the diary entry."""
        return f"{self.user.name}'s entry on {self.entry_date}"
    
    @classmethod
    def get_entry_for_date(cls, user, date=None):
        """
        Get a diary entry for a specific date in the user's timezone.
        If no date is provided, use current date in user's timezone.
        Returns None if no entry exists.
        """
        if date is None:
            # Get current date in user's timezone
            user_tz = pytz.timezone(user.timezone)
            date = timezone.now().astimezone(user_tz).date()
        
        try:
            return cls.objects.get(user=user, entry_date=date)
        except cls.DoesNotExist:
            return None
