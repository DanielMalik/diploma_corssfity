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
from django.conf.urls import url, include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from crossfity.views import AddAthleteUserView, AthleteLog, AddCoachUserView, CoachLog, CoachVerification, \
    CoachApplivationsView, CoachApplivationView, CoachApplivationDeleteView, CoachProfile, ApiEndpoint, \
    secret_page

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/hello', ApiEndpoint.as_view()),
    url(r'^secret$', secret_page, name='secret'),
    url(r'^logout/$', logout_then_login, name='site-logout'),
    url(r'^createuser/?$', AddAthleteUserView.as_view(), name='create-new-athlete-user'),
    url(r'^accounts/login/?$', AthleteLog.as_view(), name='athlete-login'),
    url(r'^newcoach?$', CoachVerification.as_view(), name='coach-verification'),
    url(r'^coach/?$', CoachProfile.as_view(), name='coach-profile'),
    url(r'^ctr_coach/(?P<apl_code>\d+)/(?P<pass_mails>.+)/$', AddCoachUserView.as_view(), name='create-new-coach-user'),
    url(r'^accounts/login_coach?$', CoachLog.as_view(), name='coach-login'),
    url(r'^coachapplication/?$', CoachApplivationsView.as_view(), name='review-coach-applicants'),
    url(r'^coachapplicationaccept/(?P<pk>\d+)/?$', CoachApplivationView.as_view(), name='review-coach-applicants-accept'),
    url(r'^coachapplicationdelete/(?P<pk>\d+)/?$', CoachApplivationDeleteView.as_view(), name='review-coach-applicants-delete'),
]
