from datetime import date
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    logout,
    login,
)

from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import (
    render,
    redirect
)

from django.core.files.storage import FileSystemStorage

from .forms import (
    RegistrationForm,
    UserAuthenticationForm,
)

from .models import *
from .utils import *


def main_page(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return render(request, 'main_page.html')


def registration_view(request):
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=raw_pass)

            login(request, user)

            calendar_to_user = CalendarApp(owner=user)
            calendar_to_user.save()

            messages.success(request, "Вы были зарегистрированы как {}".format(request.user.email))

            return redirect("profile")

        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже")
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, "registration.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Выход выполнен")
    return redirect("main_page")


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("profile")

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Авторизация завершена")
            return redirect("profile")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже")
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form

    return render(request, "login.html", context)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "profile/detail.html", {})


def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = PasswordChangeForm(user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже")
            context['change_password_form'] = form
    else:
        form = PasswordChangeForm(user=request.user)
        context['change_password_form'] = form

    return render(request, "profile/change_password.html", context)


def calendar_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.GET:
        try:
            get_date = date(
                *list(
                    reversed(
                        list(
                            map(
                                lambda x: int(x), request.GET['date'].split('-')
                            )
                        )
                    )
                )
            )
            return redirect('doings_day', get_date.year, get_date.month, get_date.day)
        except Exception:
            messages.error(request, 'Неправильный формат даты, правильный: dd-mm-yyyy')

    return render(request, 'calendar/date_selector.html', context)


def doings_list_view(request, year, month, day):

    doings = Doing.objects.filter(calendar_app=CalendarApp.objects.filter(owner=request.user)[0],
                                  start_time=date(year, month, day))

    context = {
        'doings': doings,
        'year': year,
        'month': month,
        'day': day
    }

    return render(request, "calendar/doings_archive_day.html", context)


def append_doing(request, year, month, day):
    Doing.objects.create(calendar_app=filter_by_owner(CalendarApp, request.user),
                         doing_type=DoingType.objects.create(),
                         start_time=date(year, month, day))

    return redirect("doings_day", year, month, day)


def delete_doings(request, year, month, day):
    Doing.objects.filter(calendar_app=filter_by_owner(CalendarApp, request.user),
                         start_time=date(year, month, day)).delete()

    return redirect("doings_day", year, month, day)


def doing_view(request, doing_id):
    if not request.user.is_authenticated:
        return redirect('login')

    doing = Doing.objects.get(pk=doing_id)

    context = {
        'doing': doing,
    }

    return render(request, 'calendar/doing/detail.html', context)


def change_doing_name(request, doing_id):
    doing = Doing.objects.get(pk=doing_id)

    if request.POST:
        doing.name = request.POST['doing_name']

        doing.save()

        return redirect('doing', doing_id)

    return render(request, 'base.html', {})


def calendar_note_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return note_view(request, 'calendar/note.html')


def calendar_note_edit_text_view(request, note_id):
    return note_edit_text_view(request, note_id, 'calendar/note.html')


def calendar_note_edit_image_view(request, note_id):
    return note_edit_image_view(request, note_id, 'calendar/note.html')


def calendar_note_delete_view(request, note_id):
    return note_delete_view(request, note_id, 'calendar/note.html')
