from django import forms

class YouTubeUrlForm(forms.Form):
    url = forms.URLField( label='URL',
        widget=forms.URLInput(attrs={'placeholder': 'Enter the YouTube URL'}))
    
    