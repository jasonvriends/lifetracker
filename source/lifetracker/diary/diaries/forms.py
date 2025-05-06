from django import forms
from django.utils import timezone
import pytz
from datetime import date

from .models import Diary

class DiaryForm(forms.ModelForm):
    """Form for creating and editing diary entries."""
    
    entry_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input input-bordered w-full'}),
        label="Date",
        help_text="Select the date for this entry"
    )
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        max_length=255
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 10}),
    )
    
    class Meta:
        model = Diary
        fields = ["entry_date", "title", "content"]
    
    def __init__(self, user=None, *args, **kwargs):
        """Initialize the form with the user to set the default date."""
        self.user = user
        super().__init__(*args, **kwargs)
        
        # If it's a new entry (not editing), set the default date to today in user's timezone
        if user and not kwargs.get('instance'):
            user_tz = pytz.timezone(user.timezone)
            today = timezone.now().astimezone(user_tz).date()
            self.fields['entry_date'].initial = today
    
    def clean_entry_date(self):
        """Validate that the entry date is valid and not in the future."""
        entry_date = self.cleaned_data.get('entry_date')
        
        # Get today's date in user's timezone
        user_tz = pytz.timezone(self.user.timezone) if self.user else pytz.UTC
        today = timezone.now().astimezone(user_tz).date()
        
        # Check if date is in the future
        if entry_date > today:
            raise forms.ValidationError("You cannot create entries for future dates.")
        
        # Check if user already has an entry for this date (only when creating new entry)
        if not self.instance.pk and Diary.objects.filter(user=self.user, entry_date=entry_date).exists():
            raise forms.ValidationError("You already have an entry for this date.")
            
        return entry_date 