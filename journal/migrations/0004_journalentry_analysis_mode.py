# Generated by Django 5.1.5 on 2025-01-20 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_alter_journalentry_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='analysis_mode',
            field=models.CharField(choices=[('therapist', 'Therapist'), ('writing_coach', 'Writing Coach'), ('reflection_guide', 'Reflection Guide'), ('growth_mentor', 'Growth Mentor')], default='therapist', help_text='Type of AI analysis to perform', max_length=20),
        ),
    ]
