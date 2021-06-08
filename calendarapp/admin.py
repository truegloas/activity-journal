from django.contrib import admin

from . import models
from .models import CalendarApp


admin.site.register(CalendarApp)
admin.site.register(models.Role)
admin.site.register(models.User)
admin.site.register(models.Note)
admin.site.register(models.LoadMeasurementType)
admin.site.register(models.Load)
admin.site.register(models.RealizeStep)
admin.site.register(models.DoingType)
admin.site.register(models.Doing)
