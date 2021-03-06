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
    UserUpdatePassword,
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
        form = UserUpdatePassword(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
        else:
            messages.error(request, "Пожалуйста, проверьте входные данные")
            context['change_password_form'] = form
    else:
        form = UserUpdatePassword(user=request.user)
        context['change_password_form'] = form

    return render(request, "profile/change_password.html", context)


def calendar_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.GET:
        try:
            get_date = extract_date_from_str(request.GET['date'])
            return redirect('doings_day', get_date.year, get_date.month, get_date.day)
        except Exception:
            messages.error(request, 'Данная ошибка неизвестна, свяжитесь с администратором')

    return render(request, 'calendar/date_selector.html', context)


def doings_list_view(request, year, month, day):

    doings = Doing.objects.filter(calendar_app=CalendarApp.objects.filter(owner=request.user)[0],
                                  start_time=date(year, month, day))

    year, month, day = date_formatter(year, month, day)

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
    steps = RealizeStep.objects.filter(doing=doing)

    year, month, day = date_formatter(
        doing.start_time.year,
        doing.start_time.month,
        doing.start_time.day
    )

    context = {
        'doing': doing,
        'year': year,
        'month': month,
        'day': day,
        'steps': steps,
    }

    return render(request, 'calendar/doing/steps_archive_day.html', context)


def change_doing_name(request, doing_id):
    doing = Doing.objects.get(pk=doing_id)

    if request.POST:
        doing.name = request.POST['doing_name']

        doing.save()

        return redirect('doing', doing_id)

    return render(request, 'stopper.html')


def change_doing_date(request, doing_id):
    doing = Doing.objects.get(pk=doing_id)

    if request.POST:
        try:
            doing.start_time = extract_date_from_str(request.POST['doing_date'])
            doing.save()

            return redirect('doing', doing_id)
        except Exception:
            messages.error(request, 'Неправильный формат даты, правильный: dd-mm-yyyy')
            pass

        return redirect('doing', doing_id)


def change_doing_type_name(request, year, month, day, doing_type_id):
    doing_type = DoingType.objects.get(pk=doing_type_id)

    if request.POST:
        doing_type.name = request.POST['doing_type_name']

        doing_type.save()

        return redirect('doings_day', year, month, day)

    return render(request, 'stopper.html')


def append_step(request, doing_id):
    RealizeStep.objects.create(doing=Doing.objects.get(pk=doing_id),
                               load=Load.objects.create(
                                   load_measurement_type=LoadMeasurementType.objects.create()
                               ))

    return redirect("doing", doing_id)


def delete_steps(request, doing_id):
    RealizeStep.objects.filter(doing=Doing.objects.get(pk=doing_id)).delete()

    return redirect("doing", doing_id)


def step_view(request, step_id):
    if not request.user.is_authenticated:
        return redirect('login')

    step = RealizeStep.objects.get(pk=step_id)

    context = {
        'step': step,
    }

    return render(request, 'calendar/doing/step/detail.html', context)


def change_step_name(request, step_id):
    step = RealizeStep.objects.get(pk=step_id)

    if request.POST:
        step.name = request.POST['step_name']

        step.save()

        return redirect('step', step_id)

    return render(request, 'stopper.html')


def change_step_start_time(request, doing_id, step_id):
    step = RealizeStep.objects.get(pk=step_id)

    if request.POST:
        try:
            step_start_time = datetime.time.fromisoformat(request.POST['step_start_time' + str(step_id)])

            if step_start_time > step.end_time:
                messages.error(request, 'Начальное время не может быть позже конечного')
                return redirect('doing', doing_id)

            step.start_time = step_start_time
            step.save()
        except TypeError:
            messages.error(request, 'Неправильный формат времени')
            pass

        return redirect('doing', doing_id)


def change_step_end_time(request, doing_id, step_id):
    step = RealizeStep.objects.get(pk=step_id)

    if request.POST:
        try:
            step.end_time = datetime.time.fromisoformat(request.POST['step_end_time' + str(step_id)])
            step.save()
        except Exception:
            messages.error(request, 'Неправильный формат времени')
            pass

        return redirect('doing', doing_id)


def change_load_measurement_type_name(request, step_id, load_measurement_type_id):
    load_measurement_type = LoadMeasurementType.objects.get(pk=load_measurement_type_id)

    if request.POST:
        load_measurement_type.name = request.POST['load_measurement_type_name']

        load_measurement_type.save()

        return redirect('step', step_id)

    return render(request, 'stopper.html')


def change_realized_load(request, step_id):
    step = RealizeStep.objects.get(pk=step_id)

    if request.POST:
        step.load.realized_load = request.POST['realized_load']
        step.load.save()
        pass
    return redirect('step', step_id)


def change_target_load(request, step_id):
    step = RealizeStep.objects.get(pk=step_id)

    if request.POST:
        step.load.target_load = request.POST['target_load']
        step.load.save()
        pass
    return redirect('step', step_id)


def calendar_note_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    try:
        note = Note.objects.get(
            calendar_app=filter_by_owner(CalendarApp, request.user),
        )
        context['note'] = note
        return render(request, 'calendar/note.html', context)
    except Exception:
        Note.objects.create(
            calendar_app=filter_by_owner(CalendarApp, request.user),
        )
        messages.success(request, 'Заметка успешно создана')

        return redirect('calendar')
        pass


def calendar_note_edit_text_view(request, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.text = request.POST['note_text']
        note.save()

        context['note'] = note

        return render(request, 'calendar/note.html', context)

    return render(request, 'stopper.html')


def calendar_note_edit_image_view(request, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST and request.FILES:
        file = request.FILES['note_image']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        note.image = file
        note.save()

        context['note'] = note

        return render(request, 'calendar/note.html', context)

    return render(request, 'stopper.html')


def calendar_note_delete_view(request, note_id):
    Note.objects.get(pk=note_id).delete()

    messages.success(request, 'Заметка успешно удалена')

    return redirect('calendar')


def doing_note_view(request, doing_id):
    context = {}

    try:
        note = Note.objects.get(
            doing=Doing.objects.get(pk=doing_id),
        )
        context['note'] = note
        context['doing_id'] = doing_id
        return render(request, 'calendar/doing/note.html', context)
    except Exception:
        Note.objects.create(
            doing=Doing.objects.get(pk=doing_id),
        )
        messages.success(request, 'Заметка успешно удалена')

        return redirect('doing', doing_id)


def doing_note_edit_text_view(request, doing_id, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.text = request.POST['note_text']
        note.save()

        context['note'] = note
        context['doing_id'] = doing_id

        return redirect('doing_note', doing_id)

    return render(request, 'stopper.html')


def doing_note_edit_image_view(request, doing_id, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST and request.FILES:
        file = request.FILES['note_image']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        note.image = file
        note.save()

        context['note'] = note
        context['doing_id'] = doing_id

        return redirect('doing_note', doing_id)

    return render(request, 'stopper.html')


def doing_note_delete_view(request, doing_id, note_id):
    Note.objects.get(pk=note_id).delete()

    messages.success(request, 'Заметка успешно удалена')

    return redirect('doing', doing_id)


def step_note_view(request, step_id):
    context = {}

    try:
        note = Note.objects.get(
            realize_step=RealizeStep.objects.get(pk=step_id),
        )
        context['note'] = note
        context['step_id'] = step_id
        return render(request, 'calendar/doing/step/note.html', context)
    except Exception:
        Note.objects.create(
            realize_step=RealizeStep.objects.get(pk=step_id),
        )
        messages.success(request, 'Заметка успешно создана')

        return redirect('step', step_id)


def step_note_edit_text_view(request, step_id, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.text = request.POST['note_text']
        note.save()

        context['note'] = note
        context['step_id'] = step_id

        return redirect('step_note', step_id)

    return render(request, 'stopper.html')


def step_note_edit_image_view(request, step_id, note_id):
    context = {}

    note = Note.objects.get(pk=note_id)

    if request.POST and request.FILES:
        file = request.FILES['note_image']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        note.image = file
        note.save()

        context['note'] = note
        context['step_id'] = step_id

        return redirect('step_note', step_id)

    return render(request, 'stopper.html')


def step_note_delete_view(request, step_id, note_id):
    Note.objects.get(pk=note_id).delete()

    messages.success(request, 'Заметка успешно удалена')

    return redirect('step', step_id)
