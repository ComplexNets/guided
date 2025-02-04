from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import JournalEntry, UserProfile
from .forms import JournalEntryForm, UserProfileForm
from .ai_feedback import get_ai_feedback
from django.conf import settings

@login_required
def home(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/home.html', {
        'entries': entries,
        'active_entry': None
    })

@login_required
def new_entry(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            # Only analyze if explicitly requested
            action = request.POST.get('action', 'save')
            if action == 'analyze':
                try:
                    entry.feedback = get_ai_feedback(entry.content, request.user)
                    messages.success(request, "AI feedback generated successfully!")
                except Exception as e:
                    entry.feedback = "AI feedback could not be generated at this time."
                    messages.warning(request, str(e))
            entry.save()
            return redirect('journal:entry_edit', pk=entry.pk)
    else:
        form = JournalEntryForm()
    
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/entry_form.html', {
        'form': form,
        'entries': entries,
        'active_entry': None,
        'openai_model': settings.OPENAI_MODEL
    })

@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            # Only analyze if explicitly requested
            action = request.POST.get('action', 'save')
            if action == 'analyze' or (action == 'save' and form.has_changed() and 'content' in form.changed_data and entry.feedback):
                try:
                    entry.feedback = get_ai_feedback(entry.content, request.user)
                    messages.success(request, "AI feedback generated successfully!")
                except Exception as e:
                    entry.feedback = "AI feedback could not be generated at this time."
                    messages.warning(request, str(e))
            entry.save()
            return redirect('journal:entry_edit', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/entry_form.html', {
        'form': form,
        'entries': entries,
        'active_entry': entry
    })

@login_required
def delete_entry(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
        entry.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('journal:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
        # Add dark theme styling to form fields
        form.fields['username'].widget.attrs.update({'class': 'form-control bg-dark text-light'})
        form.fields['password1'].widget.attrs.update({'class': 'form-control bg-dark text-light'})
        form.fields['password2'].widget.attrs.update({'class': 'form-control bg-dark text-light'})
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update basic information
        profile.age = request.POST.get('age')
        profile.occupation = request.POST.get('occupation')
        
        # Update personality dimensions
        profile.openness = request.POST.get('openness')
        profile.conscientiousness = request.POST.get('conscientiousness')
        profile.extraversion = request.POST.get('extraversion')
        profile.agreeableness = request.POST.get('agreeableness')
        profile.neuroticism = request.POST.get('neuroticism')
        
        # Update personal information
        profile.goals = request.POST.get('goals')
        profile.interests = request.POST.get('interests')
        profile.values = request.POST.get('values')
        profile.activities = request.POST.get('activities')
        profile.background = request.POST.get('background')
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('journal:profile')
    
    # Prepare personality traits for the template
    personality_traits = {
        'openness': profile.openness or 0,
        'conscientiousness': profile.conscientiousness or 0,
        'extraversion': profile.extraversion or 0,
        'agreeableness': profile.agreeableness or 0,
        'neuroticism': profile.neuroticism or 0
    }
    
    return render(request, 'journal/profile.html', {
        'profile': profile,
        'personality_traits': personality_traits
    })
