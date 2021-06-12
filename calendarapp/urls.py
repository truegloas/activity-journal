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
    path('calendar/note/', calendar_note_view, name='calendar_note'),
    path('calendar/note/<int:note_id>/edit_text/', calendar_note_edit_text_view, name='calendar_note_edit_text'),
    path('calendar/note/<int:note_id>/edit_image/', calendar_note_edit_image_view, name='calendar_note_edit_image'),
    path('calendar/note/<int:note_id>/delete/', calendar_note_delete_view, name='calendar_note_delete'),

    path('calendar/<int:year>/<int:month>/<int:day>/', doings_list_view, name='doings_day'),
    path('calendar/doing/<int:doing_id>/', doing_view, name='doing'),
    path('calendar/doing/<int:doing_id>/change_name/', change_doing_name, name='change_doing_name'),
    path('calendar/doing/<int:doing_id>/change_date/', change_doing_date, name='change_doing_date'),

    path('calendar/doing/<int:doing_id>/note/', doing_note_view, name='doing_note'),
    path('calendar/doing/<int:doing_id>/note/<int:note_id>/edit_text/', doing_note_edit_text_view, name='doing_note_edit_text'),
    path('calendar/doing/<int:doing_id>/note/<int:note_id>/edit_image/', doing_note_edit_image_view, name='doing_note_edit_image'),
    path('calendar/doing/<int:doing_id>/note/<int:note_id>/', doing_note_delete_view, name='doing_note_delete'),

    path('calendar/append_doing/<int:year>/<int:month>/<int:day>/', append_doing, name='append_doing'),
    path('calendar/delete_doings/<int:year>/<int:month>/<int:day>/', delete_doings, name='delete_doings'),

    path('calendar/step/<int:step_id>/', step_view, name='step'),
    path('calendar/step/<int:step_id>/change_name/', change_step_name, name='change_step_name'),
    path('calendar/doing/<int:doing_id>/step/<int:step_id>/change_start_time/', change_step_start_time, name='change_step_start_time'),
    path('calendar/doing/<int:doing_id>/step/<int:step_id>/change_end_time/', change_step_end_time, name='change_step_end_time'),

    path('calendar/doing/<int:doing_id>/append_step/', append_step, name='append_step'),
    path('calendar/doing/<int:doing_id>/delete_steps/', delete_steps, name='delete_steps'),

    path('calendar/step/<int:step_id>/change_realized_load', change_realized_load, name='change_realized_load'),
    path('calendar/step/<int:step_id>/change_target_load', change_target_load, name='change_target_load'),

    path('calendar/step/<int:step_id>/note/', step_note_view, name='step_note'),
    path('calendar/step/<int:step_id>/note/<int:note_id>/edit_text/', step_note_edit_text_view, name='step_note_edit_text'),
    path('calendar/step/<int:step_id>/note/<int:note_id>/edit_image/', step_note_edit_image_view, name='step_note_edit_image'),
    path('calendar/step/<int:step_id>/note/<int:note_id>/', step_note_delete_view, name='step_note_delete'),
]
