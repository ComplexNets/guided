from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class JournalEntry(models.Model):
    ANALYSIS_MODES = [
        ('therapist', 'Therapist'),
        ('writing_coach', 'Writing Coach'),
        ('reflection_guide', 'Reflection Guide'),
        ('growth_mentor', 'Growth Mentor'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Journal entry content in HTML format")
    feedback = models.TextField(blank=True, null=True)
    analysis_mode = models.CharField(
        max_length=20, 
        choices=ANALYSIS_MODES,
        default='therapist',
        help_text="Type of AI analysis to perform"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Journal entries'

    def __str__(self):
        return self.title
