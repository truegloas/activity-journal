from django.contrib import messages, admin
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

from .forms import (
    RegistrationForm,
    UserAuthenticationForm,
    UserUpdatePassword,
)

from .models import CalendarApp


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
            context['setpassword_form'] = form
    else:
        form = PasswordChangeForm(user=request.user)
        context['setpassword_form'] = form

    return render(request, "profile/change_password.html", context)


def calendar_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
