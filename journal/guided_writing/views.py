from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import GuidedProgram, GuidedSession, UserGuidedProgress, GuidedEntry
from .feedback import get_guided_feedback

@login_required
def program_list(request):
    """Display available guided writing programs"""
    programs = GuidedProgram.objects.all()
    user_progress = UserGuidedProgress.objects.filter(user=request.user)
    
    # Combine program info with user progress
    program_status = []
    for program in programs:
        progress = user_progress.filter(program=program).first()
        program_status.append({
            'program': program,
            'progress': progress,
            'completed': progress.completed if progress else False,
            'current_session': progress.current_session if progress else 1
        })
    
    return render(request, 'guided_writing/program_list.html', {
        'program_status': program_status
    })

@login_required
def start_program(request, program_id):
    """Start or resume a guided writing program"""
    program = get_object_or_404(GuidedProgram, id=program_id)
    
    # Get or create user progress
    progress, created = UserGuidedProgress.objects.get_or_create(
        user=request.user,
        program=program,
        defaults={'current_session': 1}
    )
    
    if created:
        messages.success(request, f"Welcome to {program.name}!")
    
    return redirect('guided_writing:guided_session', program_id=program.id, session_number=progress.current_session)

@login_required
def guided_session(request, program_id, session_number):
    """Handle a specific guided writing session"""
    program = get_object_or_404(GuidedProgram, id=program_id)
    session = get_object_or_404(GuidedSession, program=program, session_number=session_number)
    progress = get_object_or_404(UserGuidedProgress, user=request.user, program=program)
    
    # Don't allow skipping ahead
    if session_number > progress.current_session:
        messages.warning(request, "Please complete the previous sessions first.")
        return redirect('guided_writing:guided_session', program_id=program.id, session_number=progress.current_session)
    
    # Get existing entry if any
    entry = GuidedEntry.objects.filter(
        user=request.user,
        program=program,
        session=session
    ).first()
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        action = request.POST.get('action', 'save')
        
        if not content:
            messages.warning(request, "Please write something before saving.")
            return render(request, 'guided_writing/session.html', {'program': program, 'session': session, 'entry': entry})
        
        # Create or update entry
        if not entry:
            entry = GuidedEntry(user=request.user, program=program, session=session)
        
        entry.content = content
        
        # Generate feedback if requested
        if action == 'analyze':
            try:
                entry.feedback = get_guided_feedback(
                    content,
                    program.name.lower().replace(' ', '_'),
                    session_number,
                    user=request.user
                )
                messages.success(request, "Feedback generated successfully!")
            except Exception as e:
                messages.warning(request, str(e))
        
        entry.save()
        
        # If this was the last session and it's complete, mark the program as finished
        if session_number == program.total_sessions and entry.feedback:
            progress.completed = True
            progress.completed_at = timezone.now()
            messages.success(request, f"Congratulations! You've completed {program.name}!")
        # Otherwise, update progress to next session if we're on the current session
        elif session_number == progress.current_session and entry.feedback:
            progress.current_session = min(session_number + 1, program.total_sessions)
        
        progress.save()
        
        return redirect('guided_writing:guided_session', program_id=program.id, session_number=session_number)
    
    return render(request, 'guided_writing/session.html', {
        'program': program,
        'session': session,
        'entry': entry,
        'is_final_session': session_number == program.total_sessions
    })
