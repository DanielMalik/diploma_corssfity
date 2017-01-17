from django.shortcuts import render
from django.utils import timezone
from crossfity.models import Coach, Athlete
from crossfity.forms import AddAthleteUser, AddCoachUser, AthleteLogin, CoachLogin

from django.shortcuts import render, redirect
from django.views import View

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


# Create your views here.

class AddAthleteUserView(View):
    def get(self, request):
        form = AddAthleteUser
        return render(request, 'crossfity/new_athlete.html', {'form': form})

    def post(self, request):
        form = AddAthleteUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(password)
            password2 = form.cleaned_data['password2']
            print(password2)
            first_name = form.cleaned_data['f_name']
            last_name = form.cleaned_data['l_name']
            email = form.cleaned_data['e_mail']
            if password == password2:
                user = authenticate(username=username,
                                    password=password)
                if user is None:
                    new_user = User.objects.create_user(username, email, password)
                    new_user.username = username
                    new_user.password = password
                    new_user.email = email
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.save()
                    new_athlete = Athlete.objects.create(user=User.objects.get(username=username))
                    new_athlete.save()
                    print(new_user)
                    print(new_athlete)
                    return render(request, 'crossfity/thanks.html')
                else:
                    form.add_error(None, "user exists")
                    return render(request, "crossfity/new_athlete.html", {"form": form})

            else:
                form.add_error(None, "match error")
                return render(request, "crossfity/new_athlete.html", {"form": form})


        else:
            form.add_error(None, "ERROR")
            return render(request, "crossfity/new_athlete.html", {"form": form})


class AddCoachUserView(View):
    def get(self, request):
        form = AddCoachUser
        return render(request, 'crossfity/new_coach.html', {'form': form})

    def post(self, request):
        form = AddCoachUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(password)
            password2 = form.cleaned_data['password2']
            print(password2)
            first_name = form.cleaned_data['f_name']
            last_name = form.cleaned_data['l_name']
            email = form.cleaned_data['e_mail']
            if password == password2:
                user = authenticate(username=username,
                                    password=password)
                if user is None:
                    new_user = User.objects.create_user(username, email, password)
                    new_user.username = username
                    new_user.password = password
                    new_user.email = email
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.save()
                    new_athlete = Coach.objects.create(user=User.objects.get(username=username))
                    new_athlete.save()
                    print(new_user)
                    print(new_athlete)
                    return render(request, 'crossfity/thanks.html')
                else:
                    form.add_error(None, "user exists")
                    return render(request, "crossfity/new_coach.html", {"form": form})

            else:
                form.add_error(None, "match error")
                return render(request, "crossfity/new_coach.html", {"form": form})


        else:
            form.add_error(None, "ERROR")
            return render(request, "crossfity/new_coach.html", {"form": form})


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
