from django import forms

from crossfity.models import CoachApplication
from django.forms import ModelForm
from django.utils import timezone
from crossfity import models


# Create your views here.

class AddAthleteUser(forms.Form):
    username = forms.CharField(max_length=128, label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password")
    f_name = forms.CharField(max_length=128, label="Name")
    l_name = forms.CharField(max_length=128, label="Surname")
    e_mail = forms.EmailField(label="e-mail")

class CoachAuthenticationForm(ModelForm):
    class Meta:
        model = CoachApplication
        fields = '__all__'
        widgets = {'application_date': forms.HiddenInput(), 'status': forms.HiddenInput()}

class AddCoachUser(forms.Form):
    username = forms.CharField(max_length=128, label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password")
    f_name = forms.CharField(max_length=128, label="Name")
    l_name = forms.CharField(max_length=128, label="Surname")
    e_mail = forms.EmailField(label="e-mail")

class AthleteLogin(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

class CoachLogin(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)