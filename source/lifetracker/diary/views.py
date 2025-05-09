from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, date, timedelta
import json
import zoneinfo
import logging

from .models import Diary, Ingredient
from .forms import DiaryForm

logger = logging.getLogger(__name__)

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
    
    # Convert to UTC for database query
    utc = zoneinfo.ZoneInfo('UTC')
    start_datetime_utc = start_datetime_local.astimezone(utc)
    end_datetime_utc = end_datetime_local.astimezone(utc)
    
    # Get entries for the selected date
    diary_entries = Diary.objects.select_related('user').prefetch_related('ingredients').filter(
        user=request.user,
        recorded_at__gte=start_datetime_utc,
        recorded_at__lte=end_datetime_utc
    ).order_by('-recorded_at', '-created_at')  # Sort by recorded_at first, then created_at as a tiebreaker
    
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
    
    # Get user's timezone
    user_tz = zoneinfo.ZoneInfo(request.user.timezone)
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST)
        
        if form.is_valid():
            # Log ingredients data for debugging
            logger.debug(f"Ingredients input data: {form.cleaned_data.get('ingredients_input')}")
            
            # Get the cleaned recorded_at value, which should already be timezone-aware in UTC
            recorded_at = form.cleaned_data.get('recorded_at')
            
            try:
                # Create diary entry and save it
                diary_entry = form.save()
                
                # Log saved ingredients for debugging
                logger.debug(f"Saved ingredients: {list(diary_entry.ingredients.values_list('name', flat=True))}")
                
                messages.success(request, "Diary entry created successfully.")
                
                # Redirect back to the original date the user was viewing
                redirect_date = original_date if original_date else timezone.localtime(recorded_at, timezone=user_tz).date().strftime('%Y-%m-%d')
                return redirect(f"{reverse('diary:list')}?date={redirect_date}")
            except Exception as e:
                logger.error(f"Error saving diary entry: {str(e)}")
                messages.error(request, "Error saving diary entry. Please try again.")
        else:
            # Log form errors for debugging
            logger.debug(f"Form errors: {form.errors}")
    else:
        # Pre-fill date if it's passed in query string
        initial = {}
        date_str = request.GET.get('date')
        if date_str:
            try:
                # Convert the date string to a datetime at the current time
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                current_time = timezone.localtime(timezone.now(), timezone=user_tz).time()
                
                # Combine the selected date with current time in user's timezone
                initial_datetime = timezone.make_aware(
                    datetime.combine(selected_date, current_time),
                    timezone=user_tz
                )
                initial['recorded_at'] = initial_datetime
            except ValueError:
                pass
        
        form = DiaryForm(request.user, initial=initial)
    
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
    
    # Handle favorite toggle action
    if request.method == 'POST' and request.POST.get('action') == 'toggle_favorite':
        diary_entry.favorite = request.POST.get('favorite') == 'true'
        diary_entry.save(update_fields=['favorite'])
        return JsonResponse({'status': 'success'})
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST, instance=diary_entry)
        
        if form.is_valid():
            # Log ingredients data for debugging
            logger.debug(f"Ingredients input data: {form.cleaned_data.get('ingredients_input')}")
            
            # Get the cleaned recorded_at value, which should already be timezone-aware
            recorded_at = form.cleaned_data.get('recorded_at')
            
            # Update and save the entry
            updated_entry = form.save()
            
            # Log saved ingredients for debugging
            logger.debug(f"Saved ingredients: {list(updated_entry.ingredients.values_list('name', flat=True))}")
            
            messages.success(request, "Diary entry updated successfully.")
            
            # Redirect back to the original date the user was viewing
            return redirect(f"{reverse('diary:list')}?date={original_date}")
        else:
            # Log form errors for debugging
            logger.debug(f"Form errors: {form.errors}")
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

@login_required
def favorites(request):
    """Return a list of favorite diary entries."""
    favorites = Diary.objects.select_related('user').prefetch_related('ingredients').filter(
        user=request.user,
        favorite=True
    ).order_by('-recorded_at')
    
    favorite_data = []
    for entry in favorites:
        # Get ingredients as a list of names
        ingredients = list(entry.ingredients.values_list('name', flat=True))
        
        favorite_data.append({
            'id': entry.id,
            'title': entry.title,
            'content': entry.content,
            'category': entry.category,
            'ingredients': json.dumps(ingredients) if ingredients else None,
            'recorded_at': entry.recorded_at.isoformat()
        })
    
    return JsonResponse(favorite_data, safe=False) 