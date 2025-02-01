from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JournalEntry

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

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
