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
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', logoutUser, name='logout'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^auth/$', UserAuthentication.as_view(), name='authenticate'),
    url(r'^home/$', home, name='home'),
    url(r'^postjob/$', PostJobAPIView.as_view(), name='postjob'),
    path('applyjob/<int:pk>/', applyJob, name='applyjob'),
    path('applicants/<int:pk>/', applicants, name='applicants'),
    path('applications/', applications, name='applications'),
    path('jobs/', jobs, name='jobs'),
    path('delete/', delete, name='delete'),
    path('giveProfile/', giveProfile, name='delete'),
    url(r'^updateprofile/$', UpdateProfileAPIView.as_view(), name='updateprofile'),
]