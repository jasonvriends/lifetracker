from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, date, timedelta
import zoneinfo

from .models import Diary
from .forms import DiaryForm

@login_required
def diary_list(request):
    """View to list diary entries with pagination and date filtering."""
    
    # Get selected date or default to today in user's timezone
    selected_date_str = request.GET.get('date')
    
    # Get user's timezone
    user_tz = zoneinfo.ZoneInfo(request.user.timezone)
    
    if selected_date_str:
        try:
            # Parse the date from request
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            # If invalid date, default to today in user's timezone
            selected_date = timezone.localtime(timezone.now(), timezone=user_tz).date()
    else:
        # Default to today in user's timezone
        selected_date = timezone.localtime(timezone.now(), timezone=user_tz).date()
    
    # Get today's date (for max date in date picker)
    today = timezone.localtime(timezone.now(), timezone=user_tz).date()
    today_formatted = today.strftime('%Y-%m-%d')
    
    # Calculate previous and next day for navigation
    prev_date = (selected_date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (selected_date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get the start and end of the selected date in user's timezone
    start_datetime_local = timezone.make_aware(
        datetime.combine(selected_date, datetime.min.time()),
        timezone=user_tz
    )
    
    end_datetime_local = timezone.make_aware(
        datetime.combine(selected_date, datetime.max.time()),
        timezone=user_tz
    )
    
    # Get entries for the selected date
    diary_entries = Diary.objects.filter(
        user=request.user,
        recorded_at__gte=start_datetime_local,
        recorded_at__lte=end_datetime_local
    ).order_by('-recorded_at')
    
    # Paginate the entries
    paginator = Paginator(diary_entries, 10)  # Show 10 entries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Format date for the form
    formatted_date = selected_date.strftime('%Y-%m-%d')
    
    context = {
        'page_obj': page_obj,
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'today_formatted': today_formatted,
        'today': today,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    
    return render(request, 'diary/diary_list.html', context)

@login_required
def diary_create(request):
    """View to create a new diary entry."""
    
    # Store the original date the user was viewing
    original_date = request.GET.get('date')
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST)
        
        if form.is_valid():
            # Get the cleaned recorded_at value, which should already be timezone-aware
            recorded_at = form.cleaned_data.get('recorded_at')
            
            # Ensure we're using the user's timezone consistently
            user_tz = zoneinfo.ZoneInfo(request.user.timezone)
            
            # Create diary entry but don't save yet
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            
            # Make sure recorded_at is timezone aware in the user's timezone
            if recorded_at and not timezone.is_aware(recorded_at):
                diary_entry.recorded_at = timezone.make_aware(recorded_at, timezone=user_tz)
            else:
                diary_entry.recorded_at = recorded_at
                
            # Save the entry
            diary_entry.save()
            
            messages.success(request, "Diary entry created successfully.")
            
            # Redirect back to the original date the user was viewing
            redirect_date = original_date if original_date else timezone.localtime(timezone.now(), timezone=user_tz).date().strftime('%Y-%m-%d')
            return redirect(f"{reverse('diary:list')}?date={redirect_date}")
    else:
        # Pre-fill date if it's passed in query string
        initial = {}
        date_str = request.GET.get('date')
        if date_str:
            try:
                # Convert the date string to a datetime at the current time
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                user_tz = zoneinfo.ZoneInfo(request.user.timezone)
                current_time = timezone.localtime(timezone.now(), timezone=user_tz).time()
                
                # Combine the selected date with current time
                initial_datetime = timezone.make_aware(
                    datetime.combine(selected_date, current_time),
                    timezone=user_tz
                )
                initial['recorded_at'] = initial_datetime
            except ValueError:
                pass
                
        form = DiaryForm(request.user, initial=initial)
    
    # Pass the original date to the template so we can use it in form submission
    return render(request, 'diary/diary_form.html', {
        'form': form,
        'is_create': True,
        'original_date': original_date
    })

@login_required
def diary_update(request, pk):
    """View to update an existing diary entry."""
    
    # Store the original date the user was viewing
    original_date = request.GET.get('date')
    
    diary_entry = get_object_or_404(Diary, pk=pk, user=request.user)
    user_tz = zoneinfo.ZoneInfo(request.user.timezone)
    
    # If no original date was provided, use the entry's date
    if not original_date:
        original_date = timezone.localtime(diary_entry.recorded_at, timezone=user_tz).date().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST, instance=diary_entry)
        
        if form.is_valid():
            # Get the cleaned recorded_at value, which should already be timezone-aware
            recorded_at = form.cleaned_data.get('recorded_at')
            
            # Ensure we're using the user's timezone consistently
            user_tz = zoneinfo.ZoneInfo(request.user.timezone)
            
            # Create diary entry but don't save yet
            updated_entry = form.save(commit=False)
            
            # Make sure recorded_at is timezone aware in the user's timezone
            if recorded_at and not timezone.is_aware(recorded_at):
                updated_entry.recorded_at = timezone.make_aware(recorded_at, timezone=user_tz)
            else:
                updated_entry.recorded_at = recorded_at
                
            # Save the entry
            updated_entry.save()
            
            messages.success(request, "Diary entry updated successfully.")
            
            # Redirect back to the original date the user was viewing
            return redirect(f"{reverse('diary:list')}?date={original_date}")
    else:
        form = DiaryForm(request.user, instance=diary_entry)
    
    return render(request, 'diary/diary_form.html', {
        'form': form,
        'diary_entry': diary_entry,
        'is_create': False,
        'original_date': original_date
    })

@login_required
def diary_delete(request, pk):
    """View to delete a diary entry."""
    
    # Store the original date the user was viewing
    original_date = request.GET.get('date')
    
    diary_entry = get_object_or_404(Diary, pk=pk, user=request.user)
    user_tz = zoneinfo.ZoneInfo(request.user.timezone)
    
    # If no original date was provided, use the entry's date
    if not original_date:
        original_date = timezone.localtime(diary_entry.recorded_at, timezone=user_tz).date().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        diary_entry.delete()
        messages.success(request, "Diary entry deleted successfully.")
        return redirect(f"{reverse('diary:list')}?date={original_date}")
    
    return render(request, 'diary/diary_confirm_delete.html', {
        'diary_entry': diary_entry,
        'original_date': original_date
    }) 