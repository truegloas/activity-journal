from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change_password/', views.change_password_view, name='change_password'),
    path('calendar', views.calendar_view, name='calendar'),
]
