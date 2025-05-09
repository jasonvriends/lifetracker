from django import forms
from django.utils import timezone
from datetime import date, datetime
import json
import zoneinfo
import logging

from .models import Diary, Ingredient

logger = logging.getLogger(__name__)

class DiaryForm(forms.ModelForm):
    """Form for creating and editing diary entries."""
    
    CATEGORY_CHOICES = [
        ('eat', 'Eat'),
        ('drink', 'Drink'),
        ('exercise', 'Exercise'),
    ]
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.HiddenInput(),  # Hidden because we'll use tabs instead
        initial='eat'  # Default to 'eat'
    )
    
    recorded_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local', 
            'class': 'input input-bordered w-full',
            'step': '60',  # 1 minute step
            'placeholder': 'Select date and time'
        }),
        label="Date and Time",
        help_text="Select the date and time for this entry (in your timezone)",
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']
    )
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        max_length=255,
        label="Name"
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
        label="Notes",
        required=False,
        help_text="Optional notes for this entry"
    )
    
    favorite = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'toggle toggle-primary',
            'role': 'switch',
        }),
        label="Favorite"
    )

    ingredients_input = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Ingredients"
    )
    
    class Meta:
        model = Diary
        fields = ["category", "recorded_at", "title", "content", "favorite", "ingredients_input"]
    
    def __init__(self, user=None, *args, **kwargs):
        """Initialize the form with the user to set the default date and time."""
        self.user = user
        
        # Get user's timezone with fallback to UTC
        try:
            self.user_tz = zoneinfo.ZoneInfo(user.timezone if user else 'UTC')
            if user:
                logger.debug(f"Using timezone {self.user_tz} for user {user.id}")
        except zoneinfo.ZoneInfoNotFoundError:
            logger.warning(f"Invalid timezone {user.timezone if user else 'None'} for user {user.id if user else 'None'}, falling back to UTC")
            self.user_tz = zoneinfo.ZoneInfo('UTC')
        
        # Ensure we have initial data
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
            
        # For new entries without a recorded_at value, set to current time
        if not kwargs.get('instance') and 'recorded_at' not in kwargs['initial']:
            current_time = timezone.now()
            local_time = timezone.localtime(current_time, self.user_tz)
            kwargs['initial']['recorded_at'] = local_time
            logger.debug(f"Setting initial recorded_at to current time: {local_time}")
        
        super().__init__(*args, **kwargs)
        
        if not user:
            logger.warning("No user provided for DiaryForm initialization")
            return
        
        # For existing entries, ensure recorded_at is in local time
        if self.instance and self.instance.pk and self.instance.recorded_at:
            # Get the UTC time from the instance
            utc_time = self.instance.recorded_at
            # Convert to local time
            local_time = timezone.localtime(utc_time, self.user_tz)
            # Set both initial and current value
            self.initial['recorded_at'] = local_time
            self.fields['recorded_at'].widget.attrs['value'] = local_time.strftime('%Y-%m-%dT%H:%M')
            logger.debug(f"Setting initial recorded_at from instance: {local_time}")
            
        # Handle ingredients
        if self.instance and self.instance.pk and self.instance.ingredients.exists():
            ingredients = list(self.instance.ingredients.values_list('name', flat=True))
            self.initial['ingredients_input'] = json.dumps(ingredients)
            logger.debug(f"Setting initial ingredients: {ingredients}")

    def clean_recorded_at(self):
        """Convert the local datetime to UTC for storage."""
        recorded_at = self.cleaned_data.get('recorded_at')
        if recorded_at:
            # Always treat the input as being in the user's timezone
            if timezone.is_naive(recorded_at):
                # Make the datetime aware in the user's timezone
                recorded_at = timezone.make_aware(recorded_at, self.user_tz)
                logger.debug(f"Made naive recorded_at aware in user timezone: {recorded_at}")
            else:
                # If it's already aware, ensure it's in the user's timezone
                recorded_at = recorded_at.astimezone(self.user_tz)
                logger.debug(f"Converted aware recorded_at to user timezone: {recorded_at}")
            
            # Convert to UTC for storage using zoneinfo
            utc_tz = zoneinfo.ZoneInfo('UTC')
            utc_recorded_at = recorded_at.astimezone(utc_tz)
            logger.debug(f"Converted recorded_at to UTC: {utc_recorded_at}")
            return utc_recorded_at
        return recorded_at

    def save(self, commit=True):
        """Save the diary entry and handle ingredients."""
        instance = super().save(commit=False)
        
        # Set the user before saving
        if self.user and not instance.user_id:
            instance.user = self.user
        
        # Save the instance first
        instance.save()
        
        # Handle ingredients
        ingredients_data = self.cleaned_data.get('ingredients_input', '[]')
        try:
            ingredient_names = json.loads(ingredients_data)
        except json.JSONDecodeError:
            ingredient_names = []
        
        # Clear existing ingredients if any
        instance.ingredients.clear()
        
        # Create or get ingredients and add them to the entry
        for name in ingredient_names:
            if name.strip():  # Only process non-empty names
                try:
                    ingredient, _ = Ingredient.objects.get_or_create(
                        user=self.user,
                        name=name.strip()
                    )
                    instance.ingredients.add(ingredient)
                except Exception:
                    pass  # Skip any problematic ingredients
        
        # Call save_m2m() from parent form to handle other m2m relationships
        if hasattr(self, 'save_m2m'):
            self.save_m2m()
        
        return instance 