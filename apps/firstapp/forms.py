from django.forms.fields import DateField
from django import forms
import datetime



class dateForm(forms.Form):
    birthdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
