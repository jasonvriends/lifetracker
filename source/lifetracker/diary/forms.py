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
        
        if not user:
            return
            
        # Get user's timezone
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
            
        # For existing entries
        elif kwargs.get('instance'):
            instance = kwargs.get('instance')
            if instance and instance.recorded_at:
                # Convert stored UTC time to user's local time
                local_time = timezone.localtime(instance.recorded_at, timezone=user_tz)
                
                # Format for datetime-local input
                formatted_datetime = local_time.strftime('%Y-%m-%dT%H:%M')
                
                # Set both initial and widget value
                self.fields['recorded_at'].initial = local_time
                self.fields['recorded_at'].widget.format = '%Y-%m-%dT%H:%M'
                self.fields['recorded_at'].widget.attrs['value'] = formatted_datetime
    
    def clean_recorded_at(self):
        """Clean the recorded_at field to ensure proper timezone handling."""
        recorded_at = self.cleaned_data.get('recorded_at')
        
        if not recorded_at or not self.user:
            return recorded_at
            
        # Get user's timezone
        user_tz = zoneinfo.ZoneInfo(self.user.timezone)
        
        # The datetime from the form will be naive - make it timezone aware
        if timezone.is_naive(recorded_at):
            # Interpret the naive datetime as being in the user's timezone
            recorded_at = timezone.make_aware(recorded_at, timezone=user_tz)
        
        # Convert to UTC for storage
        return recorded_at.astimezone(zoneinfo.ZoneInfo("UTC")) 