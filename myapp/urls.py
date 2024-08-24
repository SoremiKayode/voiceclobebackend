from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('convert', views.convert, name='convert'),
    path('profile', views.profile, name='profile'),
    path('all-profiles', views.all_profiles, name='all_profiles'),
    path('all-audio', views.all_audio, name='all_audio'),
    path('logout', views.logout, name='logout'),
]
