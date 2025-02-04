from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    goals = models.TextField(blank=True, help_text="Personal goals and aspirations")
    
    # Big 5 Personality Dimensions (0-100 scale)
    openness = models.IntegerField(default=50, help_text="Openness to Experience")
    conscientiousness = models.IntegerField(default=50)
    extraversion = models.IntegerField(default=50)
    agreeableness = models.IntegerField(default=50)
    neuroticism = models.IntegerField(default=50)
    
    # Additional biographical information
    occupation = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    values = models.TextField(blank=True, help_text="Personal values and beliefs")
    activities = models.TextField(blank=True, help_text="Regular activities and hobbies")
    background = models.TextField(blank=True, help_text="Historical background and experiences")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class JournalEntry(models.Model):
    ANALYSIS_MODES = [
        ('therapist', 'CBT Therapist'),
        ('mindfulness', 'Mindfulness Counselor'),
        ('reflection', 'Reflection Guide'),
        ('growth', 'Growth Mentor'),
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
