from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views


urlpatterns = [
    path('',home,name='home'),    
    path('register/',registerUser,name='register'),
    path('apply/<int:pk>/',applyPage,name='apply'),
    path('hire/<int:pk>/',hireCandidates,name='hire'),
    path('profile/deleteAccount/', deleteAccount, name='deleteAccount'),
    path('deleteAccount/delete', delete, name='del'),
    path('postjob/',postjob.as_view(),name='postjob'),
    path('<int:pk>/', jobdetail.as_view(), name='jobdetail'),
    path('<int:pk>/jobupdate',jobupdate.as_view(),name='jobupdate'),
    path('<int:pk>/jobdelete/', jobdelete.as_view(), name='jobdelete'),
    #path('<int:pk>/applypage',applypage.as_view(),name='applypage'),
    path('admin/', admin.site.urls),    
    path('profile/',profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('applicants/<int:pk>/',applicants,name='applicants'),
    path('applications/',applications,name='applications'),     
    path('jobs/', jobs, name='jobs'),
    path('profileUpdate/',profileUpdate,name='profileUpdate'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)