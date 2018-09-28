from django import forms
from django.utils.safestring import mark_safe

class CardForm(forms.Form):
    card_text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':40, 'cols':75}))
    
