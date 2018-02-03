"""diploma_crossfity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from crossfity.views import AddAthleteUserView, AthleteLog, AddCoachUserView, CoachLog, CoachVerification, \
    CoachApplivationsView, CoachApplicationView, CoachApplivationDeleteView, CoachProfile, AthleteProfile




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^api/hello', ApiEndpoint.as_view()),
    # url(r'^secret$', secret_page, name='secret'),
    url(r'^logout/$', logout_then_login, name='site-logout'),
    url(r'^createuser/?$', AddAthleteUserView.as_view(), name='create-new-athlete-user'),
    url(r'^accounts/login/?$', AthleteLog.as_view(), name='athlete-login'),
    url(r'^newcoach?$', CoachVerification.as_view(), name='coach-verification'),
    url(r'^coach/?$', CoachProfile.as_view(), name='coach-profile'),
    url(r'^ctr_coach/(?P<apl_code>\d+)/(?P<pass_mails>.+)/$', AddCoachUserView.as_view(), name='create-new-coach-user'),
    url(r'^accounts/login_coach?$', CoachLog.as_view(), name='coach-login'),
    url(r'^coachapplication/?$', CoachApplivationsView.as_view(), name='review-coach-applicants'),
    url(r'^coachapplicationaccept/(?P<pk>\d+)/?$', CoachApplicationView.as_view(), name='review-coach-applicants-accept'),
    url(r'^coachapplicationdelete/(?P<pk>\d+)/?$', CoachApplivationDeleteView.as_view(), name='review-coach-applicants-delete'),
    url(r'^athlete/?$', AthleteProfile.as_view(), name='athlete-profile'),
]
