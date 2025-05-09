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
            'step': '60'  # 1 minute step
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
        super().__init__(*args, **kwargs)
        
        if not user:
            return
            
        # Get user's timezone from their profile
        user_tz = zoneinfo.ZoneInfo(user.timezone)
        
        # If it's a new entry (not editing)
        if not kwargs.get('instance'):
            # Get current time in UTC
            utc_now = timezone.now()
            # Convert to user's timezone
            local_now = timezone.localtime(utc_now, timezone=user_tz)
            
            # Format for datetime-local input (HTML5 standard)
            formatted_datetime = local_now.strftime('%Y-%m-%dT%H:%M')
            
            # Set both initial and widget value
            self.fields['recorded_at'].initial = local_now
            self.fields['recorded_at'].widget.format = '%Y-%m-%dT%H:%M'
            self.fields['recorded_at'].widget.attrs['value'] = formatted_datetime
        else:
            # For existing entries, set the ingredients_input value
            instance = kwargs['instance']
            if instance.ingredients.exists():
                # Prefetch ingredients to avoid multiple queries
                ingredients = list(instance.ingredients.values_list('name', flat=True))
                logger.debug(f"Initializing form with existing ingredients: {ingredients}")
                self.fields['ingredients_input'].initial = json.dumps(ingredients)
            else:
                logger.debug("No existing ingredients found for this entry")
                self.fields['ingredients_input'].initial = '[]'

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