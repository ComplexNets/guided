from django.db import models
from django.contrib.auth.models import User

class GuidedProgram(models.Model):
    """Represents a guided writing program (e.g., Expressive Writing, CBT Workbook)"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_sessions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GuidedSession(models.Model):
    """Represents a specific session within a guided program"""
    program = models.ForeignKey(GuidedProgram, on_delete=models.CASCADE, related_name='sessions')
    session_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['session_number']
        unique_together = ['program', 'session_number']

    def __str__(self):
        return f"{self.program.name} - Session {self.session_number}: {self.title}"

class UserGuidedProgress(models.Model):
    """Tracks a user's progress through guided writing programs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(GuidedProgram, on_delete=models.CASCADE)
    current_session = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'program']

    def __str__(self):
        return f"{self.user.username}'s progress in {self.program.name}"

class GuidedEntry(models.Model):
    """Represents a user's response to a guided writing session"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(GuidedProgram, on_delete=models.CASCADE)
    session = models.ForeignKey(GuidedSession, on_delete=models.CASCADE)
    content = models.TextField()
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Guided entries'

    def __str__(self):
        return f"{self.user.username}'s entry for {self.session}"
