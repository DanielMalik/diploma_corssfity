from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from crossfity.models import CoachApplication, Coach


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
        fields = [
            'name', 'surname', 'certification', 'e_mail', 'phone_number', 'description', 'application_date', 'status',
        ]
        widgets = {'application_date': forms.HiddenInput(), 'status': forms.HiddenInput()}


class CoachApplicationStatus(ModelForm):
    class Meta:
        model = CoachApplication
        fields = ['status', 'pass_mail', 'pass_phone']
        widgets = {'pass_mail': forms.HiddenInput(), 'pass_phone': forms.HiddenInput()}


class AddCoachUser(ModelForm):
    class Meta:
        model = Coach
        fields = '__all__'
        exclude = ['user']


class AthleteLogin(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class CoachLogin(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
