from django import forms

class APIKeyForm(forms.Form):
    api_key = forms.CharField(label='API Key', max_length=255)
    api_secret = forms.CharField(label='API Secret', max_length=255, widget=forms.PasswordInput)

