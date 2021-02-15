from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import *
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserAuthentication
    )

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='loginAPI'),
    url(r'^logout/$', logoutUser, name='logoutAPI'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='registerAPI'),
    url(r'^auth/$', UserAuthentication.as_view(), name='authenticate'),
    url(r'^home/$', home, name='homeAPI'),
    url(r'^postjob/$', PostJobAPIView.as_view(), name='postjobAPI'),
    path('applyjob/<int:pk>/', applyJob, name='applyjobAPI'),
    path('applicants/<int:pk>/', applicants, name='applicantsAPI'),
    path('applications/', applications, name='applicationsAPI'),
    path('jobs/', jobs, name='jobsAPI'),
    path('delete/', delete, name='deleteAPI'),
    path('giveProfile/', giveProfile, name='giveProfileAPI'),
    url(r'^updateprofile/$', UpdateProfileAPIView.as_view(), name='updateprofileAPI'),
]