from django import forms

# Create your models here.
class ProjectModel(forms.Form):
    Category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: heritage'}))
    Region  = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: north'}))
    Budget  = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: 30 (in thousands)'}))