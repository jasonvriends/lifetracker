from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib import messages
import pytz
from datetime import datetime, date

from .models import Diary
from .forms import DiaryForm

@login_required
def diary_list(request):
    """View to list diary entries with pagination and date filtering."""
    
    # Get user's timezone
    user_tz = pytz.timezone(request.user.timezone)
    
    # Get selected date or default to today
    selected_date_str = request.GET.get('date')
    
    if selected_date_str:
        try:
            # Parse the date from request
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            # If invalid date, default to today
            selected_date = timezone.now().astimezone(user_tz).date()
    else:
        # Default to today in user's timezone
        selected_date = timezone.now().astimezone(user_tz).date()
    
    # Get today's date (for max date in date picker)
    today = timezone.now().astimezone(user_tz).date()
    today_formatted = today.strftime('%Y-%m-%d')
    
    # Get entries for the selected date
    diary_entries = Diary.objects.filter(
        user=request.user,
        entry_date=selected_date
    ).order_by('-created_at')
    
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
    }
    
    return render(request, 'diaries/diary_list.html', context)

@login_required
def diary_create(request):
    """View to create a new diary entry."""
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST)
        
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()
            
            messages.success(request, "Diary entry created successfully.")
            return redirect('diaries:list')
    else:
        # Pre-fill date if it's passed in query string
        initial = {}
        date_str = request.GET.get('date')
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                initial['entry_date'] = selected_date
            except ValueError:
                pass
                
        form = DiaryForm(request.user, initial=initial)
    
    return render(request, 'diaries/diary_form.html', {
        'form': form,
        'is_create': True
    })

@login_required
def diary_update(request, pk):
    """View to update an existing diary entry."""
    
    diary_entry = get_object_or_404(Diary, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DiaryForm(request.user, request.POST, instance=diary_entry)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Diary entry updated successfully.")
            return redirect('diaries:list')
    else:
        form = DiaryForm(request.user, instance=diary_entry)
    
    return render(request, 'diaries/diary_form.html', {
        'form': form,
        'diary_entry': diary_entry,
        'is_create': False
    })

@login_required
def diary_delete(request, pk):
    """View to delete a diary entry."""
    
    diary_entry = get_object_or_404(Diary, pk=pk, user=request.user)
    
    if request.method == 'POST':
        diary_entry.delete()
        messages.success(request, "Diary entry deleted successfully.")
        return redirect('diaries:list')
    
    return render(request, 'diaries/diary_confirm_delete.html', {
        'diary_entry': diary_entry
    })
