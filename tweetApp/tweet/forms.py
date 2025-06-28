from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': (
                    'block w-full bg-gray-800 text-white border border-gray-600 '
                    'rounded-lg p-4 mt-1 focus:outline-none focus:ring-2 '
                    'focus:ring-indigo-500 placeholder-gray-400'
                ),
                'rows': 4,
                'placeholder': 'What’s happening?'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': (
                    'block w-[60%] text-white bg-gray-800 border border-gray-600 '
                    'rounded-lg p-3 mt-1 cursor-pointer focus:outline-none '
                    'focus:ring-2 focus:ring-indigo-500'
                )
            }),
        }
        labels = {
            'text': 'Tweet Text',
            'photo': 'Upload Photo',
        }



class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(
    
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
      


        

