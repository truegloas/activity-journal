from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .models import *


def filter_by_owner(model, user):
    return model.objects.filter(owner=user)[0]


def note_view(request, render_page, context=None):
    if context is None:
        context = {}
        pass

    note = Note.objects.get(
        calendar_app=filter_by_owner(CalendarApp, request.user)
    )

    if not note:
        Note.objects.create(
            calendar_app=filter_by_owner(CalendarApp, request.user)
        )
        pass

    context['note'] = note

    return render(request, render_page, context)


def note_edit_text_view(request, note_id, render_page, context=None):
    if context is None:
        context = {}
        pass

    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.text = request.POST['note_text']
        note.save()

        context['note'] = note

        return render(request, render_page, context)

    return render(request, 'stopper.html')


def note_edit_image_view(request, note_id, render_page, context=None):
    if context is None:
        context = {}
        pass

    note = Note.objects.get(pk=note_id)

    if request.POST and request.FILES:
        file = request.FILES['note_image']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        note.image = file
        note.save()

        context['note'] = note

        return render(request, render_page, context)

    return render(request, 'base.html')


def note_delete_view(request, note_id, render_page, context=None):
    if context is None:
        context = {}
        pass

    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.delete()

        return redirect(request, render_page, context)

    return render(request, 'stopper.html')
