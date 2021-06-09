from datetime import date
from django.urls import path
from django.contrib import admin

from .views import *


urlpatterns = [
    path('', main_page, name='main_page'),
    path('main_page/', main_page, name='main_page'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/change_password/', change_password_view, name='change_password'),
    path('calendar/', calendar_view, name='calendar'),
    path('calendar/notes/', calendar_notes_view, name='calendar_notes'),
    path('calendar/<int:year>/<int:month>/<int:day>/', doings_list_view, name='doings_day'),
    path('calendar/doing/<int:doing_id>', doing_view, name='doing'),
    path('calendar/append_doing/<int:year>/<int:month>/<int:day>/', append_doing, name='append_doing'),
    path('calendar/delete_doings/<int:year>/<int:month>/<int:day>/', delete_doings, name='delete_doings'),
]
