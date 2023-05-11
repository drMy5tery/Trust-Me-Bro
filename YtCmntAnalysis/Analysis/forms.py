from django import forms

class YouTubeUrlForm(forms.Form):
    url = forms.URLField(label='YouTube URL')