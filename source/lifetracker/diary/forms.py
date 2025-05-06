from django import forms
from django.utils import timezone
from datetime import date, datetime
import zoneinfo

from .models import Diary

class DiaryForm(forms.ModelForm):
    """Form for creating and editing diary entries."""
    
    recorded_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local', 
            'class': 'input input-bordered w-full',
            'step': '60'  # 1 minute step
        }),
        label="Date and Time",
        help_text="Select the date and time for this entry",
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']
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
        fields = ["recorded_at", "title", "content"]
    
    def __init__(self, user=None, *args, **kwargs):
        """Initialize the form with the user to set the default date and time."""
        self.user = user
        super().__init__(*args, **kwargs)
        
        # If it's a new entry (not editing), set the default datetime to now in user's timezone
        if user and not kwargs.get('instance'):
            user_tz = zoneinfo.ZoneInfo(user.timezone)
            current_datetime = timezone.localtime(timezone.now(), timezone=user_tz)
            
            # Format for datetime-local input (HTML5 standard)
            self.fields['recorded_at'].initial = current_datetime
        elif kwargs.get('instance'):
            # For existing entries, make sure we're showing the time in user's timezone
            if user:
                user_tz = zoneinfo.ZoneInfo(user.timezone)
                instance = kwargs.get('instance')
                if instance and instance.recorded_at:
                    localized_dt = timezone.localtime(instance.recorded_at, timezone=user_tz)
                    self.initial['recorded_at'] = localized_dt 