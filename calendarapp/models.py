from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Пользователи должны иметь email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    email = models.EmailField(db_index=True, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class CalendarApp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=False,
    )


class DoingType(models.Model):
    name = models.CharField(max_length=255, default='Вид деятельности')

    def __str__(self):
        return self.name


class Doing(models.Model):
    name = models.CharField(max_length=255, default='Деятельность')

    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)

    calendar_app = models.ForeignKey(CalendarApp, on_delete=models.CASCADE, null=True, blank=True)
    doing_type = models.ForeignKey(DoingType, on_delete=models.CASCADE, null=True, blank=True, auto_created=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('doing', kwargs={'doing_id': self.pk})


class LoadMeasurementType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Load(models.Model):
    realized_load = models.DecimalField(max_digits=5, decimal_places=2)
    target_load = models.DecimalField(max_digits=5, decimal_places=2)
    load_measurement_type = models.ForeignKey(LoadMeasurementType, on_delete=models.CASCADE, null=True, blank=True)


class RealizeStep(models.Model):
    name = models.CharField(max_length=255, default="Шаг")

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    doing = models.ForeignKey(Doing, on_delete=models.CASCADE, null=True)
    load = models.ForeignKey(Load, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    text = models.CharField(max_length=63999, default="Текст заметки")
    image = models.ImageField(upload_to='images', default=None, blank=True)

    calendar_app = models.OneToOneField(
        CalendarApp, on_delete=models.CASCADE, null=True, blank=True,
    )
    doing = models.OneToOneField(
        Doing, on_delete=models.CASCADE, null=True, blank=True,
    )
    realize_step = models.OneToOneField(
        RealizeStep, on_delete=models.CASCADE, null=True, blank=True,
    )

    def get_absolute_url(self):
        return reverse('calendar_notes', kwargs={'note_id': self.pk})
