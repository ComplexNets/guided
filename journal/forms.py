from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JournalEntry, UserProfile

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'writing-title',
                'placeholder': 'Title',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'writing-content',
                'placeholder': 'Start writing...',
                'spellcheck': 'true'
            }),
        }
        labels = {
            'title': '',
            'content': ''
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'goals', 'openness', 'conscientiousness', 'extraversion', 
                 'agreeableness', 'neuroticism', 'occupation', 'interests', 'values']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'openness': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '0', 'max': '100'}),
            'conscientiousness': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '0', 'max': '100'}),
            'extraversion': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '0', 'max': '100'}),
            'agreeableness': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '0', 'max': '100'}),
            'neuroticism': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '0', 'max': '100'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'values': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'openness': 'Openness to Experience',
            'conscientiousness': 'Conscientiousness',
            'extraversion': 'Extraversion',
            'agreeableness': 'Agreeableness',
            'neuroticism': 'Neuroticism',
        }
        help_texts = {
            'goals': 'What are your main goals and aspirations?',
            'interests': 'What are your main interests and hobbies?',
            'values': 'What are your core values and beliefs?',
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-light'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light'}),
        }
