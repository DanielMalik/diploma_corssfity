from django.shortcuts import render
from django.utils import timezone
from crossfity.models import Coach, Athlete
from crossfity.forms import AddAthleteUser, AddCoachUser, AthleteLogin, CoachLogin, CoachAuthenticationForm
from crossfity.forms import CoachApplication

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.http import HttpResponse

from django.db.models import Q
import operator
import functools
from django.urls import reverse_lazy

from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView

from sendsms import api


# Create your views here.

class AddAthleteUserView(View):

    def get(self, request):
        form = UserCreationForm
        return render(request, 'crossfity/new_athlete.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            new_athlete = Athlete.objects.create(user=User.objects.get(username=username))
            new_athlete.save()
            return redirect('profile')
        else:
            form_user.add_error(None, "ERROR")
            return render(request, "crossifty/new_athlete.html", {"form": form})

# preliminary verification for new coach user - we must be sure he has at least CF Level one cert.
class CoachVerification(View):
    # anyone can access this form
    def get(self, request):
        form = CoachAuthenticationForm
        return render(request, 'crossfity/coach_verification.html', {'form': form})
    # this will write application to database - admin must review it manually and respond
    def post(self, request):
        form = CoachAuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'crossfity/apply_thanks.html')

        else:
            form_user.add_error(None, "ERROR")
            return render(request, "crossifty/coach_verification.html", {"form": form})


#     this is view of applications to coach users - for admin only - review candidates here
class CoachApplivationView(UpdateView):
    model = CoachApplication
    fields = ['name', 'certification', 'status']
    template_name_suffix = '_admin_review'
#     ok, this one can/t be generic, because i want to send him an email and sms after I confirm his cartifications.

# this needs to be blocked, access only via likn sent in e mail(with one-time token)
class AddCoachUserView(View):
    def get(self, request):
        form = UserCreationForm
        return render(request, 'crossfity/new_coach.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            new_coach = Coach.objects.create(user=User.objects.get(username=username))
            new_coach.save()
            return redirect('coach-profile')
        else:
            form_user.add_error(None, "ERROR")
            return render(request, "crossifty/new_coach.html", {"form": form})

class AthleteLog(View):

    def get(self, request):
        form = AthleteLogin()
        return render(request, 'crossfity/athlete_login.html', {'form': form})

    def post(self, request):
        form = AthleteLogin(request.POST)
        if form.is_valid():
            next = request.GET.get('next')
            data = dict()
            data['username'] = form.cleaned_data['login']
            data['password'] = form.cleaned_data['password']

            user = authenticate(username=data['username'],
                                password=data['password'])
            if user is not None:
                print('ok')
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return render(request, "crossfity/thanks.html")

            else:
                print("k.o.")
                form = AthleteLogin()
                return render(request, 'crossfity/athlete_login.html', {'form': form})


class CoachLog(View):

    def get(self, request):
        form = CoachLogin()
        return render(request, 'crossfity/coach_login.html', {'form': form})

    def post(self, request):
        form = CoachLogin(request.POST)
        if form.is_valid():
            next = request.GET.get('next')
            data = dict()
            data['username'] = form.cleaned_data['login']
            data['password'] = form.cleaned_data['password']

            user = authenticate(username=data['username'],
                                password=data['password'])
            if user is not None:
                print('ok')
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return render(request, "crossfity/thanks.html")

            else:
                print("k.o.")
                form = CoachLogin()
                return render(request, 'crossfity/coach_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'crossfity/athlete_login.html')
