from django.core.management.base import BaseCommand
from journal.guided_writing.models import GuidedProgram, GuidedSession

class Command(BaseCommand):
    help = 'Sets up initial guided writing programs'

    def handle(self, *args, **options):
        # Create Expressive Writing program
        program, created = GuidedProgram.objects.get_or_create(
            name='Expressive Writing',
            defaults={
                'description': '''A structured 4-session writing program designed to help process significant life experiences.
                Through guided reflection, you'll explore the facts, emotions, connections, and future implications of your experience.''',
                'total_sessions': 4
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Expressive Writing program'))
        
        # Create sessions
        sessions = [
            {
                'session_number': 1,
                'title': 'Writing the Facts',
                'description': '''In this first session, focus on describing what happened as objectively as possible.
                Stick to the facts: what occurred, when, where, and who was involved.
                Try to write without including your emotions or interpretations.
                Write about what happened, focusing only on the objective facts.
                What occurred? When did it happen? Where were you? Who was involved?
                Try to be as detailed and specific as possible while remaining factual.'''
            },
            {
                'session_number': 2,
                'title': 'Writing About Emotions',
                'description': '''Now explore your emotional response to the event.
                How did you feel when it happened? How do you feel about it now?
                Don't judge your emotions - simply acknowledge and express them.''',
                'prompt': '''Write about your emotional experience of the event.
                What feelings came up during the event?
                How do those feelings compare to how you feel now?
                Allow yourself to fully express all emotions, whether positive or negative.'''
            },
            {
                'session_number': 3,
                'title': 'Writing About Associations',
                'description': '''Explore how this event connects to other experiences in your life.
                Does it remind you of other situations? Has it influenced your behavior or thoughts?
                Look for patterns and connections.''',
                'prompt': '''Write about how this event connects to other parts of your life.
                Does it remind you of other experiences?
                Has it influenced your current behaviors, fears, or beliefs?
                What patterns do you notice?'''
            },
            {
                'session_number': 4,
                'title': 'Writing About Future Paths',
                'description': '''In this final session, focus on moving forward.
                How can you use this experience for growth?
                What steps can you take toward healing or positive change?''',
                'prompt': '''Write about how you can move forward from this experience.
                What have you learned?
                How might you reframe this experience?
                What specific steps can you take toward growth or healing?'''
            }
        ]
        
        for session_data in sessions:
            session, created = GuidedSession.objects.get_or_create(
                program=program,
                session_number=session_data['session_number'],
                defaults={
                    'title': session_data['title'],
                    'description': session_data['description'],
                    'prompt': session_data['prompt']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created session {session.session_number}: {session.title}'))
            
        self.stdout.write(self.style.SUCCESS('Guided writing programs setup complete!'))
