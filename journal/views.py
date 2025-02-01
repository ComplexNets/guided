from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry
from .forms import JournalEntryForm
from .ai_feedback import get_ai_feedback
from django.conf import settings

@login_required
def home(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/home.html', {'entries': entries})

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
                    mode = request.POST.get('analysis_mode', 'therapist')
                    entry.analysis_mode = mode
                    entry.feedback = get_ai_feedback(entry.content, mode=mode)
                    messages.success(request, "Entry analyzed successfully!")
                except Exception as e:
                    entry.feedback = "AI feedback could not be generated at this time."
                    messages.warning(request, str(e))
            
            entry.save()
            return redirect('edit_entry', pk=entry.pk)
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
                    mode = request.POST.get('analysis_mode', entry.analysis_mode)
                    entry.analysis_mode = mode
                    entry.feedback = get_ai_feedback(entry.content, mode=mode)
                    if action == 'analyze':
                        messages.success(request, "Entry analyzed successfully!")
                except Exception as e:
                    entry.feedback = "AI feedback could not be generated at this time."
                    messages.warning(request, str(e))
            
            entry.save()
            return redirect('edit_entry', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/entry_form.html', {
        'form': form,
        'entries': entries,
        'active_entry': entry,
        'openai_model': settings.OPENAI_MODEL
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
