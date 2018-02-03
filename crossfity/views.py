from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from crossfity.forms import AddCoachUser, AthleteLogin, CoachLogin, CoachAuthenticationForm
from crossfity.forms import CoachApplication, CoachApplicationStatus, CreateUserForm
from crossfity.models import Coach, Athlete, WOD
from crossfity.tasks import SendEmailTask


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


class CoachVerification(View):
    """ Preliminary verification for new coach user - we must be sure he has at least CF Level one cert."""

    def get(self, request):
        # anyone can access this form
        form = CoachAuthenticationForm
        return render(request, 'crossfity/coach_verification.html', {'form': form})

    def post(self, request):
        # this will write application to database - admin must review it manually and respond
        form = CoachAuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'crossfity/apply_thanks.html')
        else:
            form.add_error(None, "ERROR")
            return render(request, 'crossfity/coach_verification.html', {"form": form})


class CoachApplivationsView(PermissionRequiredMixin, View):
    """ This is view of applications to coach users - for admin only - review candidates here."""
    permission_required = "change_coachapplication"

    def get(self, request):
        return render(
            request,
            'crossfity/coachapplication_admin_review.html',
            {'aplications': CoachApplication.objects.all},
        )

    def post(self, request):
        pass


class CoachApplicationView(PermissionRequiredMixin, View):

    permission_required = "change_coachapplication"

    def get(self, request, pk):
        aplicant = CoachApplication.objects.get(pk=pk)
        form = CoachApplicationStatus(instance=aplicant)
        return render(request, 'crossfity/coachapplication_update_form.html', {'form': form, 'aplicant': aplicant})

    def post(self, request, pk):
        aplicant = CoachApplication.objects.get(pk=pk)
        form = CoachApplicationStatus(request.POST, instance=aplicant)
        if form.is_valid():
            form.save()
            if form.cleaned_data['status'] == True:
                pass_mail = User.objects.make_random_password()
                pass_phone = User.objects.make_random_password()
                apl_code_for_url = aplicant.id
                link = f'http://127.0.0.1:8000/ctr_coach/{str(apl_code_for_url)}/{pass_mail}'

                aplicant.pass_mail = pass_mail
                aplicant.pass_phone = pass_phone
                mail = aplicant.e_mail
                aplicant.save()
                send_mail(
                    'MAIL TITLE',
                    'MAIL CONTENT + LINK %s' % link,
                    'djangocrossfitytest@gmail.com',
                    [mail],
                    fail_silently=False,
                )

                return redirect('review-coach-applicants')
            else:

                return redirect('review-coach-applicants')
        else:
            return redirect('review-coach-applicants')


class CoachApplivationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "delete_coachapplication"

    model = CoachApplication
    success_url = reverse_lazy('review-coach-applicants')


class AddCoachUserView(View):

    def get(self, request, apl_code, pass_mails):
        aplication_instance = CoachApplication.objects.get(pk=apl_code)
        if pass_mails == aplication_instance.pass_mail:
            form = CreateUserForm
            form_coach = AddCoachUser()
            return render(request, 'crossfity/new_coach.html', {'form': form, 'form_coach': form_coach})
        else:
            return reverse_lazy('coach-verification')

    def post(self, request, apl_code, pass_mails):

        aplication_instance = CoachApplication.objects.get(pk=apl_code)
        form = CreateUserForm(request.POST)
        form_coach = AddCoachUser(request.POST, request.FILES)

        if form.is_valid() and form_coach.is_valid() and pass_mails == aplication_instance.pass_mail\
                and aplication_instance.pass_coach_added == False:
            username = form.cleaned_data['username']
            if not User.objects.filter(username=form.cleaned_data['username']).exists():

                if form_coach.cleaned_data['sms_code'] == aplication_instance.pass_phone:
                    form.save()

                    aplication_instance.pass_coach_added = True
                    aplication_instance.save()
                    password = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    new_coach = Coach.objects.create(user=User.objects.get(username=username))
                    new_coach.save()
                    form_coach2 = AddCoachUser(request.POST, request.FILES, instance=new_coach)
                    form_coach2.save()

                    # send confirmation email with Celery
                    user_username = str(username)
                    print('user_username ' + user_username)
                    role = 'coach'
                    SendEmailTask.delay(user_username,  role)
                    return redirect('coach-profile')
                else:
                    form.add_error(None, "ERROR - sms code")
                    return render(request, 'crossfity/new_coach.html', {"form": form, 'form_coach': form_coach})
            else:
                form.add_error(None, "ERROR - username taken")
                return render(request, 'crossfity/new_coach.html', {"form": form, 'form_coach': form_coach})
        else:
            form.add_error(None, "ERROR - form1, form2 or url")
            return render(request, 'crossfity/new_coach.html', {"form": form, 'form_coach': form_coach})


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
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return render(request, "crossfity/thanks.html")

            else:
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


class CoachProfile(View):
    def get(self, request):
        user = request.user
        try:  # only for Coach users
            coach = Coach.objects.get(user=user)
        except Coach.DoesNotExist:
            # temporary
            return HttpResponse('przekieruj, bo to nie jest Coach tylko Athlete')

        wods = WOD.objects.filter(author=coach)
        ctx = {'user': user, 'wods': wods}
        return render(request, 'crossfity/profile.html', ctx)


class AthleteProfile(View):
    def get(self, request):
        user = request.user
        try:
            athlete = Athlete.objects.get(user=user)
        except Athlete.DoesNotExist:
            # temporary
            return HttpResponse('przekieruj, bo to nie jest Athlete')
        wods = WOD.objects.filter(athletes=athlete)
        ctx = {'user': user, 'wods': wods}
        return render(request, 'crossfity/profile.html', ctx)
