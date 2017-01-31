from django.shortcuts import render
from django.utils import timezone
from crossfity.models import Coach, Athlete
from crossfity.forms import AddAthleteUser, AddCoachUser, AthleteLogin, CoachLogin, CoachAuthenticationForm
from crossfity.forms import CoachApplication, CoachApplicationStatus

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
            form.add_error(None, "ERROR")
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
            form.add_error(None, "ERROR")
            return render(request, 'crossfity/coach_verification.html', {"form": form})


#     this is view of applications to coach users - for admin only - review candidates here
class CoachApplivationsView(PermissionRequiredMixin, View):
    permission_required = "change_coachapplication"
    def get(self, request):
        ctx = {}
        ctx['aplications'] = CoachApplication.objects.all
        return render(request, 'crossfity/coachapplication_admin_review.html', ctx)

    def post(self, request):
        pass
#     admin can view all aplications, after verification gcan send mail-sms for further registration,
#  or give sttus 'pending', send feedback to aplicant with add questions
#  or delete aplication and inform applicant, can add to 'blocked' if this user is annoying

class CoachApplivationView(PermissionRequiredMixin, View): #change status of aplicatiom to

    permission_required = "change_coachapplication"


    def get(self, request, pk):
        aplicant = CoachApplication.objects.get(pk=pk)
        form = CoachApplicationStatus(instance=aplicant)

        return render(request, 'crossfity/coachapplication_update_form.html', {'form': form, 'aplicant': aplicant})
    def post(self, request, pk):
        aplicant = CoachApplication.objects.get(pk=pk)
        form = CoachApplicationStatus(request.POST, instance=aplicant)
        mail = aplicant.e_mail
        pass_mail = User.objects.make_random_password()
        print('PASSWORD is:' + pass_mail)
        phone = aplicant.phone_number
        pass_phone = User.objects.make_random_password()
        print('PASSWORD PHONE is:' + pass_phone)


        if form.is_valid():
            aplicant.pass_mail = pass_mail
            aplicant.pass_phone = pass_phone
            aplicant.save()
            form.save()

        return redirect('review-coach-applicants')

# class CoachApplivationView(UpdateView):  #change status of aplicatiom to
#     model = CoachApplication
#     fields = ['status']
#     template_name_suffix = '_update_form'
#     success_url = reverse_lazy('review-coach-applicants')

class CoachApplivationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "delete_coachapplication"

    model = CoachApplication
    success_url = reverse_lazy('review-coach-applicants')

# this needs to be blocked, access only via link sent in e mail(with one-time token)
class AddCoachUserView(View):
    def get(self, request, pass_mails):
        if pass_mails == putmailpasswordheresomehow:

            form = UserCreationForm
            form_coach = AddCoachUser()
            return render(request, 'crossfity/new_coach.html', {'form': form, 'form_coach': form_coach})
        else:
            return reverse_lazy('coach-verification')
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
