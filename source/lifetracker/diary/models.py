from django.db import models
from django.conf import settings
from django.utils import timezone
import zoneinfo

class Ingredient(models.Model):
    """Ingredient model for categorizing diary entries."""
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_ingredients"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_ingredient_per_user"
            )
        ]

    def __str__(self):
        return self.name

class Diary(models.Model):
    """Diary entry model for recording daily journal entries."""
    
    CATEGORY_CHOICES = [
        ('eat', 'Eat'),
        ('drink', 'Drink'),
        ('exercise', 'Exercise'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_entries"
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='eat'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # Make content optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    favorite = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name="diary_entries")
    
    class Meta:
        verbose_name_plural = "Diary Entries"
        ordering = ["-recorded_at", "-created_at"]
        # Ensure users can have multiple entries per date but not exact same datetime
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recorded_at"],
                name="unique_diary_entry_per_datetime"
            )
        ]
    
    def __str__(self):
        """String representation of the diary entry."""
        return f"{self.user.name}'s {self.get_category_display()} entry on {self.recorded_at}"
    
    @property
    def entry_date(self):
        """Get the date part of recorded_at for backward compatibility."""
        return self.recorded_at.date()
    
    @classmethod
    def get_entry_for_date(cls, user, date=None):
        """
        Get diary entries for a specific date in the user's timezone.
        If no date is provided, use current date in user's timezone.
        Returns queryset of entries for that date.
        """
        if date is None:
            # Get current date in user's timezone
            user_tz = zoneinfo.ZoneInfo(user.timezone)
            current_datetime = timezone.localtime(timezone.now(), timezone=user_tz)
            date = current_datetime.date()
        
        # Get the start and end of the date in user's timezone
        user_tz = zoneinfo.ZoneInfo(user.timezone)
        
        # Convert date to datetime at midnight in user's timezone
        start_datetime_local = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.min.time()),
            timezone=user_tz
        )
        
        # End of day in user's timezone
        end_datetime_local = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.max.time()),
            timezone=user_tz
        )
        
        # Convert to UTC for database query
        start_datetime_utc = timezone.make_naive(start_datetime_local, timezone=timezone.utc)
        end_datetime_utc = timezone.make_naive(end_datetime_local, timezone=timezone.utc)
        
        return cls.objects.filter(
            user=user,
            recorded_at__gte=start_datetime_utc,
            recorded_at__lte=end_datetime_utc
        ).order_by("-recorded_at") 